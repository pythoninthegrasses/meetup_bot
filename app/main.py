#!/usr/bin/env python3

import arrow
import bcrypt
import os
import pandas as pd
import sys
import time
from collections.abc import AsyncIterator
from colorama import Fore
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from db import APP_DIR, UserInfo, init_db
from decouple import config
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from icecream import ic
from jose import JWTError, jwt
from math import ceil
from meetup_query import *
from pathlib import Path
from pony.orm import db_session
from pydantic import BaseModel
from schedule import check_and_revert_snooze, get_current_schedule_time, get_schedule, snooze_schedule
from sign_jwt import main as gen_token
from slackbot import *

# verbose icecream
ic.configureOutput(includeContext=True)

# logging prefixes
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"

# env
home = Path.home()
cwd = Path.cwd()
csv_fn = config("CSV_FN", default="raw/output.csv")
json_fn = config("JSON_FN", default="raw/output.json")
tz = config("TZ", default="America/Chicago")
bypass_schedule = config("OVERRIDE", default=False, cast=bool)
DEV = config("DEV", default=False, cast=bool)

# time
current_time_local = arrow.now(tz)
current_time_utc = arrow.utcnow()
current_day = current_time_local.format("dddd")  # Monday, Tuesday, etc.
time.tzset()

# pandas don't truncate output
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)

# index
templates = Jinja2Templates(directory=APP_DIR / "resources" / "templates")

# creds
TTL = config("TTL", default=3600, cast=int)
HOST = config("HOST")
PORT = config("PORT", default=3000, cast=int)
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")
TOKEN_EXPIRE = config("TOKEN_EXPIRE", default=480, cast=int)

try:
    DB_USER = config("DB_USER")
    DB_PASS = config("DB_PASS").strip('"')
except Exception:
    print(
        f"{Fore.RED}FATAL:{Fore.RESET} DB_USER and DB_PASS environment variables are required. "
        "These credentials are used for API authentication, not database connectivity. "
        "Set them in .env or as environment variables."
    )
    sys.exit(1)

"""
IP Address Whitelisting
"""


DISABLE_IP_WHITELIST = config("DISABLE_IP_WHITELIST", default=False, cast=bool)


def _parse_public_ips() -> list[str]:
    raw = config("PUBLIC_IPS", default="")
    return [ip.strip() for ip in raw.split(",") if ip.strip()]


class IPConfig(BaseModel):
    whitelist: list[str] = ["localhost", "127.0.0.1"]
    public_ips: list[str] = []


ip_config = IPConfig(public_ips=_parse_public_ips())


def is_ip_allowed(request: Request):
    client_host = request.client.host
    return client_host in ip_config.whitelist or client_host in ip_config.public_ips


"""
FastAPI app
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize database and create default user on startup."""
    init_db()
    try:
        with db_session:
            if not UserInfo.exists(username=DB_USER):
                hashed_password = get_password_hash(DB_PASS)
                UserInfo(username=DB_USER, hashed_password=hashed_password)
    except Exception:
        pass
    yield


# main web app
app = FastAPI(
    title="meetup_bot API",
    openapi_url="/meetup_bot.json",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)

# add `/api` route in front of all other endpoints
api_router = APIRouter(prefix="/api")

# CORS
origins = [
    "http://localhost",
    "http://localhost:" + str(PORT),
    "http://127.0.0.1",
    "http://127.0.0.1:" + str(PORT),
    "http://0.0.0.0",
    "http://0.0.0.0:" + str(PORT),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
Authentication
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def verify_password(plain_password, hashed_password):
    """Validate plaintext password against hashed password"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password):
    """Return hashed password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def get_user(username: str):
    with db_session:
        user = UserInfo.get(username=username)
        if user:
            return UserInDB(username=user.username, hashed_password=user.hashed_password)


def authenticate_user(username: str, password: str):
    """Authenticate user"""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(request: Request, token: str | None = Depends(oauth2_scheme)):
    """Get current user from Bearer token or session_token cookie."""
    if token is None:
        token = request.cookies.get("session_token")
    if token is None:
        return None
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as err:
        raise credentials_exception from err
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User | None = Depends(get_current_user)):
    """Get current active user"""
    if current_user is None:
        return None
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def ip_whitelist_or_auth(request: Request, current_user: User | None = Depends(get_current_active_user)):
    if DEV or (not DISABLE_IP_WHITELIST and is_ip_allowed(request)):
        return {"bypass_auth": True}

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user


def check_auth(auth: dict | User) -> None:
    """
    Shared function to check authentication result.
    Raises an HTTPException if authentication fails.
    """
    if isinstance(auth, dict) and auth.get("bypass_auth"):
        print("Authentication bypassed due to whitelisted IP")
    elif not isinstance(auth, User):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/token", response_model=Token)
async def login_for_oauth_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login for oauth access token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    oauth_token_expires = timedelta(minutes=TOKEN_EXPIRE)
    oauth_token = create_access_token(data={"sub": user.username}, expires_delta=oauth_token_expires)

    response = JSONResponse(content={"access_token": oauth_token, "token_type": "bearer"})
    response.set_cookie(
        key="session_token",
        value=oauth_token,
        httponly=True,
        secure=not DEV,
        samesite="lax",
        max_age=TOKEN_EXPIRE * 60,
    )
    return response


"""
Login
"""


def load_user(username: str):
    with db_session:
        user = UserInfo.get(username=username)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")


"""
Startup
"""


@app.get("/healthz", status_code=200)
def health_check():
    """Smoke test to check if the app is running"""
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    with open(APP_DIR / "resources" / "templates" / "login.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.post("/auth/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Redirect to "/docs" from index page if user successfully logs in with HTML form"""
    if load_user(username) and verify_password(password, load_user(username).hashed_password):
        oauth_token_expires = timedelta(minutes=TOKEN_EXPIRE)
        oauth_token = create_access_token(data={"sub": username}, expires_delta=oauth_token_expires)
        response = RedirectResponse(url="/docs", status_code=303)
        response.set_cookie(
            key="session_token",
            value=oauth_token,
            httponly=True,
            secure=not DEV,
            samesite="lax",
            max_age=TOKEN_EXPIRE * 60,
        )
        return response


@api_router.get("/token")
def generate_token(current_user: User = Depends(get_current_active_user)):
    """
    Get access and refresh tokens

    Args:
        access_token (str): hard-coded access_token
        refresh_token (str): hard-coded refresh_token
    """

    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    global access_token, refresh_token

    # generate access and refresh tokens
    try:
        tokens = gen_token()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
    except KeyError as e:
        print(f"{Fore.RED}{error:<10}{Fore.RESET}KeyError: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

    return access_token, refresh_token


@api_router.get("/events")
def get_events(
    auth: dict | User = Depends(ip_whitelist_or_auth),
    location: str = "Oklahoma City",
    exclusions: str = "Tulsa",
):
    """
    Query upcoming Meetup events

    Args:
        location (str): location to search for events
        exclusions (str): location to exclude from search
    """

    check_auth(auth)

    access_token, refresh_token = generate_token()

    # default exclusions
    exclusion_list = [
        '36\u00b0N',
        'Bitcoin',
        'Nerdy Girls',
        'Project 3810',
    ]

    # if exclusions, add to list of exclusions
    if exclusions is not None:
        exclusions = exclusions.split(",")
        exclusion_list = exclusion_list + exclusions

    response = send_request(access_token, query, vars)
    frames = [format_response(response, exclusions=exclusion_list)]

    # third-party query (batched)
    responses = send_batched_group_request(access_token, url_vars)
    for i, response in enumerate(responses):
        df = format_response(response, exclusions=exclusion_list)
        if len(df) > 0:
            frames.append(df)
        else:
            print(f"{Fore.GREEN}{info:<10}{Fore.RESET}No upcoming events for {url_vars[i]} found")

    combined = pd.concat(frames, ignore_index=True)
    events = prepare_events(combined)

    if not events:
        return {"message": "No events found", "events": []}

    return events


@api_router.get("/check-schedule")
def should_post_to_slack(auth: dict = Depends(ip_whitelist_or_auth), request: Request = None):
    """
    Check if it's time to post to Slack based on the schedule
    """

    with db_session:
        check_and_revert_snooze()  # Check and revert any expired snoozes
        schedule = get_schedule(current_day)

        if schedule and schedule.enabled:
            utc_time, local_time = get_current_schedule_time(schedule)

            # Parse the schedule time
            schedule_time_local = (
                arrow.get(schedule.schedule_time, "HH:mm")
                .replace(year=current_time_local.year, month=current_time_local.month, day=current_time_local.day, tzinfo="UTC")
                .to(tz)
            )

            # Calculate time difference in minutes and round up
            time_diff = abs((schedule_time_local - current_time_local).total_seconds() / 60)
            time_diff_rounded = ceil(time_diff)

            # Check if current time is within n minutes of scheduled time
            should_post = time_diff_rounded <= 90

            return {
                "should_post": should_post,
                "current_time": current_time_local.format("dddd HH:mm ZZZ"),
                "schedule_time": schedule_time_local.format("dddd HH:mm ZZZ"),
                "time_diff_minutes": time_diff_rounded,
            }

        # If no schedule found or not enabled
        elif not schedule or not schedule.enabled:
            return {
                "should_post": False,
            }


@api_router.post("/slack")
def post_slack(
    auth: dict | User = Depends(ip_whitelist_or_auth),
    location: str = "Oklahoma City",
    exclusions: str = "Tulsa",
    channel_name: str = None,
    override: bool = bypass_schedule,
):
    """
    Post to slack

    Calls main function to post formatted message to predefined channel
    """

    check_auth(auth)

    events = get_events(auth=auth, location=location, exclusions=exclusions)

    # handle "no events found" response
    if isinstance(events, dict):
        events = events.get("events", [])

    msg = fmt_events(events)

    if channel_name is not None:
        channel_id = chan_dict[channel_name]
        send_message("\n".join(msg), channel_id)
    else:
        for name, id in channels.items():
            send_message("\n".join(msg), id)

    return ic(msg)


@api_router.post("/snooze")
def snooze_slack_post(
    duration: str,
    auth: dict = Depends(ip_whitelist_or_auth),
):
    """
    Snooze the Slack post for the specified duration

    Args:
        duration (str): Duration to snooze the post. Valid options are:
                        "5_minutes", "next_scheduled", "rest_of_week"
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        snooze_schedule(duration)
        return {"message": f"Slack post snoozed for {duration}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@api_router.get("/schedule")
def get_current_schedule(auth: dict | User = Depends(ip_whitelist_or_auth)):
    """
    Get the current schedule including any active snoozes
    """
    check_auth(auth)

    with db_session:
        check_and_revert_snooze()  # Check and revert any expired snoozes
        schedules = []
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            schedule = get_schedule(day)
            if schedule:
                schedules.append(
                    {
                        "day": schedule.day,
                        "schedule_time": schedule.schedule_time,
                        "enabled": schedule.enabled,
                        "snooze_until": schedule.snooze_until,
                        "original_schedule_time": schedule.original_schedule_time,
                    }
                )

    return {"schedules": schedules}


# routes
app.include_router(api_router)


def main():
    """
    Run app
    """

    import uvicorn

    try:
        uvicorn.run("main:app", host="0.0.0.0", port=PORT, limit_max_requests=10000, log_level="warning", reload=True)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
