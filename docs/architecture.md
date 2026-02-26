# Architecture

## Overview

meetup_bot queries the Meetup GraphQL API for upcoming tech community events in the
Oklahoma City area and posts formatted summaries to Slack channels on a configurable
schedule. It runs as a FastAPI web application backed by a PostgreSQL database.

## System Context

```text
+-------------------+       +---------------------+       +------------------+
|                   |       |                     |       |                  |
|  Meetup GraphQL   | <---- |    meetup_bot       | ----> |  Slack API       |
|  (gql-ext)        |       |    (FastAPI)        |       |  (Web Client)    |
|                   |       |                     |       |                  |
+-------------------+       +----------+----------+       +------------------+
                                       |
                                       v
                            +----------+----------+
                            |                     |
                            |   PostgreSQL        |
                            |   (Users + Schedule)|
                            |                     |
                            +---------------------+
```

## Application Modules

All application code lives under `app/`.

### db.py -- Shared Database Configuration

Provides a single `Database()` instance shared by all modules. The `init_db()`
function reads the `DEV` environment variable to choose the provider:

- `DEV=true` -- binds to SQLite (`db.sqlite`, created automatically)
- `DEV=false` (default) -- binds to PostgreSQL using `DB_*` env vars

`init_db()` is called during FastAPI lifespan startup, keeping database
binding out of module-level scope so imports don't require a live database.

### sign_jwt.py -- JWT Authentication with Meetup

Generates RS256-signed JWTs using a private key (PEM file or base64-encoded env var),
verifies them against the corresponding public key, and exchanges them for OAuth2
access/refresh tokens via Meetup's token endpoint. Keys are identified by
`SIGNING_KEY_ID` and scoped to `api.meetup.com`.

### meetup_query.py -- GraphQL Event Fetching

Sends two categories of GraphQL queries to `https://api.meetup.com/gql-ext`:

1. **First-party (self) query** -- fetches events from groups the authenticated user
   belongs to via `self { memberEvents }`.
2. **Third-party (group) queries** -- iterates over `groups.csv` and queries each
   group individually via `groupByUrlname(urlname:) { events }`.

Responses are filtered by city (default: Oklahoma City), excluded keywords
(e.g., "Tulsa", "Bitcoin"), and a configurable time window (`DAYS`, default 7).
Results are deduplicated, sorted by date, and exported to a JSON file. HTTP responses
are cached with `requests-cache` to reduce API calls.

### slackbot.py -- Slack Message Delivery

Reads the exported JSON, formats each event as a Slack mrkdwn bullet
(`date *group* <url|title>`), and posts the concatenated message to one or more
channels using `slack_sdk.WebClient`. Channels are mapped from `channels.csv`.

### schedule.py -- Schedule Management

Manages a `Schedule` database table (PonyORM) that controls which days and times
the bot posts. Each row stores a day of the week, a UTC schedule time, timezone,
and enabled/disabled state. Supports snooze operations (5 minutes, next scheduled,
rest of week) with automatic revert when the snooze expires.

Default enabled days: Monday, Wednesday, Friday.

### main.py -- FastAPI Application

The central web server that wires everything together.

**Routes:**

| Method | Path | Purpose |
| ------ | ---- | ------- |
| GET | `/healthz` | Health check |
| GET | `/` | Login page (HTML form) |
| POST | `/token` | OAuth2 password flow token |
| POST | `/auth/login` | Form-based login, redirects to `/docs` |
| GET | `/api/token` | Generate Meetup API tokens |
| GET | `/api/events` | Fetch and return upcoming events |
| GET | `/api/check-schedule` | Check if current time matches schedule |
| POST | `/api/slack` | Fetch events and post to Slack |
| POST | `/api/snooze` | Snooze scheduled posting |
| GET | `/api/schedule` | View full weekly schedule |

**Authentication:** Dual-layer. API routes require OAuth2 Bearer tokens (HS256 JWT
via `python-jose`). Requests from whitelisted IPs (localhost, 127.0.0.1) bypass
auth. A `UserInfo` PonyORM entity stores bcrypt-hashed credentials in PostgreSQL.

### scheduler.py -- Background Job Runner

Uses APScheduler (`BackgroundScheduler`) to periodically call the FastAPI endpoints
internally. Runs token refresh every 30 minutes and the Slack posting job on a cron
schedule. Hosts its own uvicorn instance on port 3001.

### scheduler.sh -- Shell-based Scheduler

A POSIX shell alternative to `scheduler.py`. Authenticates against the FastAPI
`/token` endpoint with curl, then hits `/api/slack` or `/api/events`. Used for
cron-based deployments.

### capture_groups.py -- Group Discovery (Playwright)

Scrapes the Meetup website with Playwright (headless Chromium) to discover
technology groups in the OKC area. Extracts group URL slugs (`urlname`) and writes
them to `groups.csv`. Run manually when the group list needs updating.

## Data Files

| File | Purpose |
| ---- | ------- |
| `groups.csv` | Meetup group URL slugs for third-party queries |
| `channels.csv` | Slack channel name-to-ID mapping |
| `meetup_queries.gql` | Reference GraphQL queries (not loaded at runtime) |
| `resources/MESSAGE.md` | Example formatted message output |
| `resources/templates/login.html` | Login page template (TwinkleCSS) |

## Database

Two tables managed by PonyORM on a single shared `Database` instance (`db.py`):

- **UserInfo** (`main.py`) -- application users (username, hashed password, email)
- **Schedule** (`schedule.py`) -- weekly posting schedule (day, time, timezone,
  enabled, snooze state)

The provider is selected at startup via the `DEV` env var: SQLite for local
development (`DEV=true`), PostgreSQL for production (`DEV=false` or unset).
The `UserInfo` table is seeded on startup with credentials from `DB_USER`/`DB_PASS`.

## Deployment

### Docker

Multi-stage build (`Dockerfile.web`):

1. **builder** -- installs uv, creates virtualenv at `/opt/venv`, installs
   dependencies from `pyproject.toml`.
2. **runner** -- slim image with a non-root `appuser`, copies the venv and app
   code, exposes the configured port, runs `startup.sh`.

`startup.sh` launches gunicorn with uvicorn workers (`-k uvicorn.workers.UvicornWorker`).

### Heroku

`heroku.yml` declares the Docker build and provisions:

- Heroku Scheduler (cron trigger)
- Heroku PostgreSQL
- Coralogix (logging)

### GitHub Container Registry

The `docker.yml` workflow builds multi-arch images (amd64, arm64) on pushes to
`main` or version tags and publishes to `ghcr.io`.

### Docker Compose

Single-service compose file for local development. Mounts `./app` as a volume and
forwards the configured port.

## CI/CD Pipelines

| Workflow | Trigger | Purpose |
| -------- | ------- | ------- |
| `pytest.yml` | PR, push | Run test suite |
| `docker.yml` | Push to main/tags | Build and publish Docker image |
| `infosec.yml` | PR, push, daily cron | Gitleaks credential scanning |
| `release-please.yml` | Push to main | Automated releases and changelogs |
| `smoke-test.yml` | PR, push | Smoke test against running container |

## Configuration

All configuration is via environment variables (loaded with `python-decouple`).
See `.env.example` for the full list. Key groups:

- **Meetup API**: `CLIENT_ID`, `CLIENT_SECRET`, `SIGNING_KEY_ID`, `SIGNING_SECRET`,
  `SELF_ID`, `PRIV_KEY_B64`, `PUB_KEY_B64`, `TOKEN_URL`, `REDIRECT_URI`
- **Slack**: `BOT_USER_TOKEN`, `USER_TOKEN`, `SLACK_WEBHOOK`, `CHANNEL`
- **Database**: `DEV` (true/false), `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`,
  `DB_PORT`, `DB_SSLMODE`
- **Application**: `HOST`, `PORT`, `SECRET_KEY`, `ALGORITHM`, `TOKEN_EXPIRE`,
  `TZ`, `DAYS`, `TTL`, `OVERRIDE`

## Key Dependencies

| Package | Role |
| ------- | ---- |
| FastAPI + uvicorn + gunicorn | Web framework and server |
| PonyORM + psycopg2 | ORM and PostgreSQL driver |
| requests + requests-cache | HTTP client with caching |
| slack-sdk | Slack Web API client |
| PyJWT + cryptography | RS256 JWT signing for Meetup auth |
| python-jose | HS256 JWT for application auth |
| arrow | Timezone-aware date/time handling |
| pandas | Data transformation and filtering |
| bcrypt | Password hashing |
| Playwright | Browser-based group discovery |
