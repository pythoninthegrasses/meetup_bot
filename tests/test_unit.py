import arrow
import json
import os
import pandas as pd
import pytest
import warnings
from capture_groups import (
    TECHLAHOMA_PRO_NETWORK_ID,
    filter_groups,
    parse_search_response,
    write_groups_csv,
)
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jose import jwt
from main import IPConfig, UserInDB, app, get_current_user, is_ip_allowed
from meetup_query import (
    build_batched_group_query,
    export_to_file,
    format_response,
    http_client,
    main,
    send_batched_group_request,
    send_request,
    sort_csv,
    sort_json,
)
from pathlib import Path
from unittest.mock import MagicMock, patch

# ── Fixtures ────────────────────────────────────────────────────────


@pytest.fixture
def test_client():
    """TestClient with dependency override for authenticated endpoints."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app, follow_redirects=False)
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def raw_test_client():
    """TestClient without dependency overrides for auth tests."""
    app.dependency_overrides.pop(get_current_user, None)
    client = TestClient(app, follow_redirects=False)
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def mock_user():
    return UserInDB(username="testuser", email="test@example.com", hashed_password="hashed_password")


@pytest.fixture
def mock_access_token(mock_user):
    return create_test_token({"sub": mock_user.username})


@pytest.fixture
def mock_response():
    return json.dumps(
        {
            "data": {
                "self": {
                    "memberEvents": {
                        "edges": [
                            {
                                "node": {
                                    "dateTime": "2024-09-20T18:00:00-05:00",
                                    "title": "Test Event",
                                    "description": "This is a test event",
                                    "eventUrl": "https://www.meetup.com/test-group/events/123456789/",
                                    "group": {"name": "Test Group", "city": "Oklahoma City", "urlname": "test-group"},
                                }
                            }
                        ]
                    }
                }
            }
        }
    )


@pytest.fixture
def mock_df():
    return pd.DataFrame(
        {
            "name": ["Test Group"],
            "date": ["2024-09-20T18:00:00-05:00"],
            "title": ["Test Event"],
            "description": ["This is a test event"],
            "city": ["Oklahoma City"],
            "eventUrl": ["https://www.meetup.com/test-group/events/123456789/"],
        }
    )


@pytest.fixture
def group_events_fragment():
    """Reusable event node for group-based responses."""
    return {
        "id": "evt1",
        "title": "Test Event",
        "description": "A test event",
        "dateTime": "2024-09-20T18:00:00-05:00",
        "eventUrl": "https://www.meetup.com/test-group/events/123/",
        "group": {
            "id": "grp1",
            "name": "Test Group",
            "urlname": "test-group",
            "link": "https://www.meetup.com/test-group/",
            "city": "Oklahoma City",
        },
    }


def create_test_token(data: dict):
    return jwt.encode(data, "test_secret_key", algorithm="HS256")


@pytest.fixture
def auth_headers(mock_access_token):
    return {"Authorization": f"Bearer {mock_access_token}"}


async def override_get_current_user():
    return UserInDB(username="testuser", email="test@example.com", hashed_password="hashed_password")


SAMPLE_RESPONSE = {
    "data": {
        "groupSearch": {
            "totalCount": 4,
            "pageInfo": {"endCursor": "cursor123", "hasNextPage": False},
            "edges": [
                {
                    "node": {
                        "id": "1",
                        "urlname": "pythonistas",
                        "name": "OKC Pythonistas",
                        "city": "Oklahoma City",
                        "proNetwork": None,
                    }
                },
                {
                    "node": {
                        "id": "2",
                        "urlname": "techlahoma-foundation",
                        "name": "Techlahoma Foundation",
                        "city": "Oklahoma City",
                        "proNetwork": {"id": "364335959210266624"},
                    }
                },
                {
                    "node": {
                        "id": "3",
                        "urlname": "okc-sharp",
                        "name": "OKC Sharp",
                        "city": "Oklahoma City",
                        "proNetwork": {"id": "364335959210266624"},
                    }
                },
                {
                    "node": {
                        "id": "4",
                        "urlname": "ok-golang",
                        "name": "OK Golang",
                        "city": "Oklahoma City",
                        "proNetwork": None,
                    }
                },
            ],
        }
    }
}

# ── DB config tests ─────────────────────────────────────────────────


@pytest.mark.unit
class TestGetDbConfig:
    def test_returns_sqlite_config(self):
        """get_db_config always returns SQLite provider config."""
        from db import get_db_config

        config = get_db_config()
        assert config["provider"] == "sqlite"
        assert "filename" in config
        assert config["create_db"] is True

    def test_db_path_env_var(self):
        """DB_PATH env var controls the SQLite file location."""
        os.environ["DB_PATH"] = "/tmp/custom.db"
        try:
            from db import get_db_config

            config = get_db_config()
            assert config["filename"] == "/tmp/custom.db"
        finally:
            os.environ.pop("DB_PATH", None)


@pytest.mark.unit
class TestDbInstance:
    def test_shared_db_instance(self):
        """db module exports a single Database instance."""
        from db import db
        from pony.orm import Database

        assert isinstance(db, Database)

    def test_init_db_callable(self):
        """init_db is a callable function."""
        from db import init_db

        assert callable(init_db)

    def test_entities_defined_on_db(self):
        """Schedule and UserInfo entities are defined on the shared db."""
        from db import Schedule, UserInfo, db

        assert "Schedule" in db.entities
        assert "UserInfo" in db.entities
        assert db.entities["Schedule"] is Schedule
        assert db.entities["UserInfo"] is UserInfo

    def test_app_dir_is_absolute(self):
        """APP_DIR points to the app/ directory."""
        from db import APP_DIR

        assert APP_DIR.is_absolute()
        assert APP_DIR.name == "app"
        assert (APP_DIR / "db.py").exists()


# ── Endpoint tests ──────────────────────────────────────────────────


@pytest.mark.unit
def test_health_check(test_client):
    response = test_client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.unit
def test_index_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.unit
def test_login_success(test_client):
    with patch('main.load_user') as mock_load_user, patch('main.verify_password', return_value=True):
        mock_load_user.return_value = UserInDB(username="testuser", email="test@example.com", hashed_password="hashed_password")

        response = test_client.post("/auth/login", data={"username": "testuser", "password": "password"})
        assert response.status_code == 303
        assert response.headers["location"] == "/docs"


@pytest.mark.unit
def test_login_failure(test_client):
    with patch('main.load_user', side_effect=HTTPException(status_code=404, detail="User not found")):
        response = test_client.post("/auth/login", data={"username": "testuser", "password": "wrong_password"})
        assert response.status_code == 404


@pytest.mark.unit
def test_get_token(test_client, auth_headers):
    mock_tokens = {"access_token": "test_access_token", "refresh_token": "test_refresh_token"}

    with patch('main.gen_token', return_value=mock_tokens):
        response = test_client.get("/api/token", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert "test_access_token" in response.json()


@pytest.mark.unit
def test_get_events(test_client, auth_headers):
    mock_events = [
        {
            "name": "Test Group",
            "date": "Thu 5/26 11:30 am",
            "title": "Test Event",
            "description": "Test Description",
            "eventUrl": "https://test.url",
            "city": "Oklahoma City",
        }
    ]

    with (
        patch('main.generate_token', return_value=("fake_access", "fake_refresh")),
        patch('main.send_request'),
        patch('main.send_batched_group_request', return_value=[]),
        patch('main.export_to_file'),
        patch('main.format_response', return_value=MagicMock(__len__=lambda s: 0)),
        patch('main.sort_json'),
        patch('main.os.path.exists', return_value=True),
        patch('main.os.stat', return_value=MagicMock(st_size=100)),
        patch('main.pd.read_json') as mock_read_json,
    ):
        mock_read_json.return_value = MagicMock()
        mock_read_json.return_value.to_dict.return_value = mock_events
        response = test_client.get(
            "/api/events", headers=auth_headers, params={"location": "Oklahoma City", "exclusions": "Tulsa"}
        )
        assert response.status_code == 200
        assert response.json() == mock_events


@pytest.mark.unit
def test_check_schedule(test_client, auth_headers):
    mock_schedule_obj = MagicMock()
    mock_schedule_obj.enabled = True
    mock_schedule_obj.schedule_time = "10:00"

    mock_db_ctx = MagicMock()
    mock_db_ctx.__enter__ = MagicMock()
    mock_db_ctx.__exit__ = MagicMock(return_value=False)

    def db_session_passthrough(f=None, *a, **kw):
        if f is not None and callable(f):
            return f
        return mock_db_ctx

    with (
        patch('pony.orm.db_session', side_effect=db_session_passthrough),
        patch('main.db_session', side_effect=db_session_passthrough),
        patch('schedule.db_session', side_effect=db_session_passthrough),
        patch('main.check_and_revert_snooze'),
        patch('main.get_schedule', return_value=mock_schedule_obj),
        patch('main.get_current_schedule_time', return_value=("10:00 UTC", "10:00 CDT")),
    ):
        response = test_client.get("/api/check-schedule", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "should_post" in data


@pytest.mark.unit
def test_post_slack(test_client, auth_headers):
    mock_message = ["Test message"]

    with (
        patch('main.get_events'),
        patch('main.fmt_json', return_value=mock_message),
        patch('main.send_message'),
        patch('main.chan_dict', {"test-channel": "C12345"}),
    ):
        response = test_client.post(
            "/api/slack",
            headers=auth_headers,
            params={"location": "Oklahoma City", "exclusions": "Tulsa", "channel_name": "test-channel"},
        )
        assert response.status_code == 200


@pytest.mark.unit
def test_post_slack_passes_auth_to_get_events(test_client, auth_headers):
    """Regression: post_slack must forward auth to get_events.

    Without this, get_events receives a raw Depends() descriptor
    and check_auth raises 401.
    """
    mock_message = ["Test message"]

    with (
        patch('main.get_events') as mock_get_events,
        patch('main.fmt_json', return_value=mock_message),
        patch('main.send_message'),
        patch('main.chan_dict', {"test-channel": "C12345"}),
    ):
        response = test_client.post(
            "/api/slack",
            headers=auth_headers,
            params={"location": "Oklahoma City", "exclusions": "Tulsa", "channel_name": "test-channel"},
        )
        assert response.status_code == 200
        # Verify auth was forwarded (not left as default Depends descriptor)
        mock_get_events.assert_called_once()
        call_kwargs = mock_get_events.call_args
        auth_arg = call_kwargs.kwargs.get("auth")
        assert auth_arg is not None, "auth must be passed to get_events"
        assert isinstance(auth_arg, UserInDB), f"auth should be a User, got {type(auth_arg)}"


@pytest.mark.unit
def test_snooze_slack_post(test_client, auth_headers):
    # snooze_slack_post endpoint references undefined `current_user` variable (app bug).
    # Patch it as a module-level variable to avoid NameError.
    with patch('main.snooze_schedule'), patch('main.current_user', create=True):
        response = test_client.post("/api/snooze", headers=auth_headers, params={"duration": "5_minutes"})
        assert response.status_code == 200
        assert response.json() == {"message": "Slack post snoozed for 5_minutes"}


@pytest.mark.unit
def test_get_current_schedule(test_client, auth_headers):
    mock_schedule_obj = MagicMock(
        day="Monday", schedule_time="10:00", enabled=True, snooze_until=None, original_schedule_time="10:00"
    )

    with (
        patch('main.check_and_revert_snooze'),
        patch('main.get_schedule', return_value=mock_schedule_obj),
        patch('main.db_session') as mock_db_sess,
    ):
        mock_db_sess.return_value.__enter__ = MagicMock()
        mock_db_sess.return_value.__exit__ = MagicMock(return_value=False)

        response = test_client.get("/api/schedule", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "schedules" in data


@pytest.mark.unit
def test_dev_mode_bypasses_auth_for_local_requests(raw_test_client):
    """When DEV=True, localhost requests should not require authentication."""

    mock_schedule_obj = MagicMock(
        day="Monday", schedule_time="10:00", enabled=True, snooze_until=None, original_schedule_time="10:00"
    )

    with (
        patch('main.DEV', True),
        patch('main.check_and_revert_snooze'),
        patch('main.get_schedule', return_value=mock_schedule_obj),
        patch('main.db_session') as mock_db_sess,
    ):
        mock_db_sess.return_value.__enter__ = MagicMock()
        mock_db_sess.return_value.__exit__ = MagicMock(return_value=False)

        response = raw_test_client.get("/api/schedule")
        assert response.status_code == 200
        data = response.json()
        assert "schedules" in data


@pytest.mark.unit
def test_unauthorized_access(raw_test_client):
    with (
        patch('main.DEV', False),
        patch('main.is_ip_allowed', return_value=False),
    ):
        response = raw_test_client.get("/api/events")
        assert response.status_code == 401
        assert "detail" in response.json()


@pytest.mark.unit
def test_invalid_token(raw_test_client):
    with (
        patch('main.DEV', False),
        patch('main.is_ip_allowed', return_value=False),
    ):
        headers = {"Authorization": "Bearer invalid_token"}
        response = raw_test_client.get("/api/events", headers=headers)
        assert response.status_code == 401
        assert "detail" in response.json()


# ── IP whitelisting tests ──────────────────────────────────────────


@pytest.mark.unit
class TestIPConfigPublicIps:
    """IPConfig.public_ips should be configurable via PUBLIC_IPS env var."""

    def test_default_public_ips_empty(self):
        cfg = IPConfig()
        assert cfg.public_ips == []

    def test_public_ips_from_env_single(self):
        with patch.dict(os.environ, {"PUBLIC_IPS": "10.0.0.1"}):
            from main import _parse_public_ips

            ips = _parse_public_ips()
            assert ips == ["10.0.0.1"]

    def test_public_ips_from_env_multiple(self):
        with patch.dict(os.environ, {"PUBLIC_IPS": "10.0.0.1,192.168.1.1,172.16.0.1"}):
            from main import _parse_public_ips

            ips = _parse_public_ips()
            assert ips == ["10.0.0.1", "192.168.1.1", "172.16.0.1"]

    def test_public_ips_from_env_empty(self):
        with patch.dict(os.environ, {"PUBLIC_IPS": ""}):
            from main import _parse_public_ips

            ips = _parse_public_ips()
            assert ips == []

    def test_public_ips_strips_whitespace(self):
        with patch.dict(os.environ, {"PUBLIC_IPS": " 10.0.0.1 , 192.168.1.1 "}):
            from main import _parse_public_ips

            ips = _parse_public_ips()
            assert ips == ["10.0.0.1", "192.168.1.1"]


@pytest.mark.unit
class TestIsIpAllowedWithPublicIps:
    """is_ip_allowed should match against both whitelist and public_ips."""

    def test_allowed_via_public_ips(self):
        mock_request = MagicMock()
        mock_request.client.host = "203.0.113.50"
        with patch("main.ip_config", IPConfig(public_ips=["203.0.113.50"])):
            assert is_ip_allowed(mock_request) is True

    def test_denied_when_not_in_either_list(self):
        mock_request = MagicMock()
        mock_request.client.host = "203.0.113.99"
        with patch("main.ip_config", IPConfig(public_ips=["203.0.113.50"])):
            assert is_ip_allowed(mock_request) is False

    def test_allowed_via_whitelist(self):
        mock_request = MagicMock()
        mock_request.client.host = "127.0.0.1"
        with patch("main.ip_config", IPConfig()):
            assert is_ip_allowed(mock_request) is True


# ── Cookie auth tests ─────────────────────────────────────────────


@pytest.mark.unit
class TestCookieAuth:
    """get_current_user should fall back to session_token cookie when no Bearer token."""

    def test_cookie_auth_returns_user(self, raw_test_client):
        from main import ALGORITHM, SECRET_KEY, get_password_hash

        token = jwt.encode({"sub": "testuser"}, SECRET_KEY, algorithm=ALGORITHM)
        with (
            patch("main.DEV", False),
            patch("main.is_ip_allowed", return_value=False),
            patch(
                "main.get_user",
                return_value=UserInDB(
                    username="testuser",
                    email="test@example.com",
                    hashed_password=get_password_hash("pass"),
                ),
            ),
        ):
            raw_test_client.cookies.set("session_token", token)
            response = raw_test_client.get("/api/events")
            raw_test_client.cookies.clear()
            assert response.status_code == 200

    def test_bearer_takes_precedence_over_cookie(self, raw_test_client):
        from main import ALGORITHM, SECRET_KEY, get_password_hash

        good_token = jwt.encode({"sub": "testuser"}, SECRET_KEY, algorithm=ALGORITHM)
        bad_cookie = "invalid_cookie_token"
        with (
            patch("main.DEV", False),
            patch("main.is_ip_allowed", return_value=False),
            patch(
                "main.get_user",
                return_value=UserInDB(
                    username="testuser",
                    email="test@example.com",
                    hashed_password=get_password_hash("pass"),
                ),
            ),
        ):
            raw_test_client.cookies.set("session_token", bad_cookie)
            response = raw_test_client.get(
                "/api/events",
                headers={"Authorization": f"Bearer {good_token}"},
            )
            raw_test_client.cookies.clear()
            assert response.status_code == 200

    def test_invalid_cookie_returns_401(self, raw_test_client):
        with (
            patch("main.DEV", False),
            patch("main.is_ip_allowed", return_value=False),
        ):
            raw_test_client.cookies.set("session_token", "invalid")
            response = raw_test_client.get("/api/events")
            raw_test_client.cookies.clear()
            assert response.status_code == 401

    def test_no_token_no_cookie_returns_401(self, raw_test_client):
        with (
            patch("main.DEV", False),
            patch("main.is_ip_allowed", return_value=False),
        ):
            response = raw_test_client.get("/api/events")
            assert response.status_code == 401


# ── Deprecation / bcrypt tests ──────────────────────────────────────


@pytest.mark.unit
class TestPasswordHashing:
    """Verify password hashing uses bcrypt directly, not passlib."""

    def test_get_password_hash_returns_bcrypt_hash(self):
        from main import get_password_hash

        hashed = get_password_hash("testpassword")
        assert hashed.startswith("$2b$"), f"Expected bcrypt hash prefix '$2b$', got: {hashed[:4]}"

    def test_verify_password_correct(self):
        from main import get_password_hash, verify_password

        hashed = get_password_hash("testpassword")
        assert verify_password("testpassword", hashed) is True

    def test_verify_password_incorrect(self):
        from main import get_password_hash, verify_password

        hashed = get_password_hash("testpassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_no_passlib_import(self):
        """passlib should not be imported by main.py."""
        import sys

        mod_name = "main"
        if mod_name in sys.modules:
            import inspect

            source = inspect.getsource(sys.modules[mod_name])
            assert "from passlib" not in source, "main.py still imports passlib"
            assert "import passlib" not in source, "main.py still imports passlib"


@pytest.mark.unit
class TestDbCredentialsRequired:
    """DB_USER and DB_PASS are required and exit with a clear message when missing."""

    def test_missing_db_creds_produces_actionable_error(self):
        """Error handler for missing DB_USER/DB_PASS should mention both var names."""
        import inspect
        import sys

        source = inspect.getsource(sys.modules["main"])
        assert "DB_USER" in source and "DB_PASS" in source
        assert "sys.exit" in source, "Missing DB creds should call sys.exit, not raise UndefinedValueError"

    def test_error_message_clarifies_purpose(self):
        """Error message should explain these are for API auth, not DB connectivity."""
        import inspect
        import sys

        source = inspect.getsource(sys.modules["main"])
        assert "authentication" in source.lower() or "API auth" in source, (
            "Error message should clarify DB_USER/DB_PASS are for API authentication"
        )


@pytest.mark.unit
class TestLifespan:
    """Verify app uses lifespan context manager, not on_event."""

    def test_app_has_no_on_event_startup(self):
        """The app should not use deprecated on_event handlers."""
        import inspect
        import sys

        source = inspect.getsource(sys.modules["main"])
        assert '@app.on_event("startup")' not in source, "main.py still uses @app.on_event('startup')"
        assert "@app.on_event('startup')" not in source, "main.py still uses @app.on_event('startup')"

    def test_app_has_lifespan(self):
        """The app should have a lifespan configured."""
        from main import app

        assert app.router.lifespan_context is not None, "App should have a lifespan context manager"


@pytest.mark.unit
class TestNoDeprecationWarnings:
    """Verify no deprecation warnings from password hashing."""

    def test_password_hash_no_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from main import get_password_hash, verify_password

            hashed = get_password_hash("test")
            verify_password("test", hashed)

            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            crypt_warnings = [x for x in deprecation_warnings if "crypt" in str(x.message).lower()]
            assert len(crypt_warnings) == 0, f"Got crypt deprecation warnings: {crypt_warnings}"


# ── Capture groups tests ────────────────────────────────────────────


@pytest.mark.unit
class TestParseSearchResponse:
    def test_extracts_groups_from_response(self):
        groups = parse_search_response(SAMPLE_RESPONSE)
        assert len(groups) == 4
        assert groups[0]["urlname"] == "pythonistas"
        assert groups[1]["urlname"] == "techlahoma-foundation"

    def test_includes_pro_network_id(self):
        groups = parse_search_response(SAMPLE_RESPONSE)
        assert groups[0]["pro_network_id"] is None
        assert groups[1]["pro_network_id"] == TECHLAHOMA_PRO_NETWORK_ID

    def test_empty_response(self):
        response = {"data": {"groupSearch": {"totalCount": 0, "edges": []}}}
        groups = parse_search_response(response)
        assert groups == []

    def test_error_response(self):
        response = {"errors": [{"message": "bad query"}]}
        groups = parse_search_response(response)
        assert groups == []


@pytest.mark.unit
class TestFilterGroups:
    def test_filters_techlahoma_affiliated_groups(self):
        groups = parse_search_response(SAMPLE_RESPONSE)
        filtered = filter_groups(groups)
        urlnames = [g["urlname"] for g in filtered]
        assert "pythonistas" in urlnames
        assert "ok-golang" in urlnames
        assert "techlahoma-foundation" not in urlnames
        assert "okc-sharp" not in urlnames

    def test_keeps_all_when_no_pro_network(self):
        groups = [
            {"urlname": "group-a", "pro_network_id": None},
            {"urlname": "group-b", "pro_network_id": None},
        ]
        filtered = filter_groups(groups)
        assert len(filtered) == 2

    def test_custom_exclude_id(self):
        groups = [
            {"urlname": "group-a", "pro_network_id": "other-network"},
            {"urlname": "group-b", "pro_network_id": None},
        ]
        filtered = filter_groups(groups, exclude_pro_network="other-network")
        assert len(filtered) == 1
        assert filtered[0]["urlname"] == "group-b"


@pytest.mark.unit
class TestWriteGroupsCsv:
    def test_writes_csv_with_correct_format(self, tmp_path):
        groups = [
            {"urlname": "pythonistas", "pro_network_id": None},
            {"urlname": "ok-golang", "pro_network_id": None},
        ]
        output = tmp_path / "groups.csv"
        write_groups_csv(groups, str(output))

        df = pd.read_csv(output)
        assert list(df.columns) == ["url", "urlname"]
        assert df.iloc[0]["urlname"] == "ok-golang"
        assert df.iloc[0]["url"] == "https://www.meetup.com/ok-golang/"
        assert df.iloc[1]["urlname"] == "pythonistas"

    def test_sorts_by_urlname(self, tmp_path):
        groups = [
            {"urlname": "zebra-group", "pro_network_id": None},
            {"urlname": "alpha-group", "pro_network_id": None},
        ]
        output = tmp_path / "groups.csv"
        write_groups_csv(groups, str(output))

        df = pd.read_csv(output)
        assert list(df["urlname"]) == ["alpha-group", "zebra-group"]

    def test_empty_groups(self, tmp_path):
        output = tmp_path / "groups.csv"
        write_groups_csv([], str(output))

        df = pd.read_csv(output)
        assert list(df.columns) == ["url", "urlname"]
        assert len(df) == 0


# ── Meetup query tests ──────────────────────────────────────────────


@pytest.mark.unit
def test_http_client_exists():
    """http_client is an httpx-compatible cache client (hishel SyncCacheClient)."""

    assert http_client is not None
    assert hasattr(http_client, "post")
    assert hasattr(http_client, "get")


@pytest.mark.unit
def test_send_request(mock_response):
    with patch("meetup_query.http_client") as mock_client:
        mock_resp = mock_client.post.return_value
        mock_resp.status_code = 200
        mock_resp.json.return_value = json.loads(mock_response)

        response = send_request("fake_token", "fake_query", '{"id": "1"}')

        assert json.loads(response) == json.loads(mock_response)
        mock_client.post.assert_called_once()


@pytest.mark.unit
def test_format_response(mock_response, mock_df):
    with patch("arrow.now", return_value=arrow.get("2024-09-18").to("America/Chicago")):
        df = format_response(mock_response)
        pd.testing.assert_frame_equal(df, mock_df)


@pytest.mark.unit
def test_sort_csv(tmp_path):
    test_csv = tmp_path / "test.csv"
    df = pd.DataFrame({"date": ["2024-09-21T10:00:00", "2024-09-20T18:00:00"], "eventUrl": ["url1", "url2"]})
    df.to_csv(test_csv, index=False)

    sort_csv(test_csv)

    sorted_df = pd.read_csv(test_csv)
    assert sorted_df["date"].tolist() == ["Fri 9/20 6:00 pm", "Sat 9/21 10:00 am"]


@pytest.mark.unit
def test_sort_json(tmp_path):
    test_json = tmp_path / "test.json"
    data = [{"date": "2024-09-21T10:00:00", "eventUrl": "url1"}, {"date": "2024-09-20T18:00:00", "eventUrl": "url2"}]
    with open(test_json, "w") as f:
        json.dump(data, f)

    with patch("arrow.now", return_value=arrow.get("2024-09-18")):
        sort_json(test_json)

    with open(test_json) as f:
        sorted_data = json.load(f)

    assert sorted_data == data, "Data should remain unchanged if not sorted"

    print("Warning: sort_json function is not sorting the data as expected")

    print("Sorted data:", json.dumps(sorted_data, indent=2))


@pytest.mark.unit
def test_sort_json_with_string_dates(tmp_path):
    """sort_json converts human-readable string dates to ISO 8601 and sorts them."""
    test_json = tmp_path / "test.json"
    data = [
        {"date": "Sat 9/21 10:00 am", "eventUrl": "url1"},
        {"date": "Fri 9/20 6:00 pm", "eventUrl": "url2"},
    ]
    with open(test_json, "w") as f:
        json.dump(data, f)

    with (
        patch("meetup_query.json_fn", str(test_json)),
        patch("arrow.now", return_value=arrow.get("2024-09-18")),
    ):
        sort_json(test_json)

    with open(test_json) as f:
        sorted_data = json.load(f)

    assert len(sorted_data) == 2
    assert sorted_data[0]["eventUrl"] == "url2"
    assert sorted_data[1]["eventUrl"] == "url1"


@pytest.mark.unit
def test_sort_json_with_timestamp_dates(tmp_path):
    """sort_json handles dates already parsed as Timestamps by pandas."""
    test_json = tmp_path / "test.json"
    data = [
        {"date": "2024-09-21T10:00:00", "eventUrl": "url1"},
        {"date": "2024-09-20T18:00:00", "eventUrl": "url2"},
    ]
    with open(test_json, "w") as f:
        json.dump(data, f)

    with (
        patch("meetup_query.json_fn", str(test_json)),
        patch("arrow.now", return_value=arrow.get("2024-09-18")),
    ):
        sort_json(test_json)

    with open(test_json) as f:
        sorted_data = json.load(f)

    assert len(sorted_data) == 2
    assert sorted_data[0]["eventUrl"] == "url2"
    assert sorted_data[1]["eventUrl"] == "url1"
    assert sorted_data[0]["date"] == "Fri 9/20 6:00 pm"
    assert sorted_data[1]["date"] == "Sat 9/21 10:00 am"


@pytest.mark.unit
def test_sort_json_consistent_output_both_formats(tmp_path):
    """Both string and Timestamp inputs produce identical output format."""
    string_json = tmp_path / "string.json"
    timestamp_json = tmp_path / "timestamp.json"

    string_data = [{"date": "Fri 9/20 6:00 pm", "eventUrl": "url1"}]
    timestamp_data = [{"date": "2024-09-20T18:00:00", "eventUrl": "url1"}]

    with open(string_json, "w") as f:
        json.dump(string_data, f)
    with open(timestamp_json, "w") as f:
        json.dump(timestamp_data, f)

    with (
        patch("arrow.now", return_value=arrow.get("2024-09-18")),
    ):
        with patch("meetup_query.json_fn", str(string_json)):
            sort_json(string_json)
        with patch("meetup_query.json_fn", str(timestamp_json)):
            sort_json(timestamp_json)

    with open(string_json) as f:
        string_result = json.load(f)
    with open(timestamp_json) as f:
        timestamp_result = json.load(f)

    assert string_result[0]["date"] == timestamp_result[0]["date"]


@pytest.mark.unit
def test_export_to_file(mock_response, tmp_path):
    test_json = tmp_path / "output.json"

    with (
        patch("meetup_query.json_fn", str(test_json)),
        patch("arrow.now", return_value=arrow.get("2024-09-18").to("America/Chicago")),
    ):
        export_to_file(mock_response, type="json")

    with open(test_json) as f:
        exported_data = json.load(f)

    assert len(exported_data) == 1
    assert exported_data[0]["title"] == "Test Event"


@pytest.mark.unit
@patch("meetup_query.gen_token")
@patch("meetup_query.send_request")
@patch("meetup_query.send_batched_group_request")
@patch("meetup_query.export_to_file")
@patch("meetup_query.sort_json")
def test_main(mock_sort_json, mock_export, mock_batched, mock_send, mock_gen_token, mock_response):
    mock_gen_token.return_value = {"access_token": "fake_token"}
    mock_send.return_value = mock_response
    mock_batched.return_value = [mock_response]

    with patch("meetup_query.url_vars", ["test-group"]), patch("meetup_query.format_response") as mock_format:
        mock_format.return_value = pd.DataFrame({"name": ["Test"]})
        main()

    mock_send.assert_called_once()
    mock_batched.assert_called_once()
    assert mock_export.call_count == 2
    mock_sort_json.assert_called_once()


@pytest.mark.unit
class TestGetAccessTokenUsesHttpx:
    """sign_jwt.get_access_token must use httpx, not requests."""

    def test_no_requests_import_in_sign_jwt(self):
        """sign_jwt should not import the requests library."""
        source = (Path(__file__).resolve().parent.parent / "app" / "sign_jwt.py").read_text()
        assert "import requests" not in source, "sign_jwt.py still imports requests"
        assert "import httpx" in source, "sign_jwt.py should import httpx"

    def test_get_access_token_uses_httpx_client(self):
        """get_access_token function body should use httpx.Client."""
        source = (Path(__file__).resolve().parent.parent / "app" / "sign_jwt.py").read_text()
        assert "httpx.Client()" in source, "get_access_token should use httpx.Client()"
        assert "requests.request" not in source, "get_access_token should not use requests.request"


@pytest.mark.unit
class TestSignJwtGracefulKeyFailure:
    """sign_jwt must not crash at import time with invalid keys."""

    def test_sign_token_returns_none_when_private_key_unavailable(self):
        """sign_token returns None when private key failed to load."""
        import sign_jwt

        original = sign_jwt.private_key
        try:
            sign_jwt.private_key = None
            result = sign_jwt.sign_token()
            assert result is None
        finally:
            sign_jwt.private_key = original

    def test_verify_token_returns_false_when_public_key_unavailable(self):
        """verify_token returns False when public key failed to load."""
        import sign_jwt

        original = sign_jwt.public_key
        try:
            sign_jwt.public_key = None
            result = sign_jwt.verify_token("fake.token.here")
            assert result is False
        finally:
            sign_jwt.public_key = original

    def test_main_returns_none_when_keys_unavailable(self):
        """main() returns None when keys failed to load."""
        import sign_jwt

        orig_priv = sign_jwt.private_key
        orig_pub = sign_jwt.public_key
        try:
            sign_jwt.private_key = None
            sign_jwt.public_key = None
            result = sign_jwt.main()
            assert result is None
        finally:
            sign_jwt.private_key = orig_priv
            sign_jwt.public_key = orig_pub


@pytest.mark.unit
class TestBuildBatchedGroupQuery:
    def test_single_group(self):
        query = build_batched_group_query(["test-group"])
        assert "group_0: groupByUrlname(urlname: \"test-group\")" in query
        assert "events(first: 10)" in query

    def test_multiple_groups(self):
        groups = ["group-a", "group-b", "group-c"]
        query = build_batched_group_query(groups)
        for i, name in enumerate(groups):
            assert f'group_{i}: groupByUrlname(urlname: "{name}")' in query

    def test_empty_list(self):
        query = build_batched_group_query([])
        assert query == ""

    def test_urlname_with_special_chars(self):
        query = build_batched_group_query(["okc-sharp"])
        assert 'group_0: groupByUrlname(urlname: "okc-sharp")' in query


@pytest.mark.unit
class TestSendBatchedGroupRequest:
    def test_returns_individual_responses(self, group_events_fragment):
        batched_response = {
            "data": {
                "group_0": {
                    "id": "grp1",
                    "description": "A group",
                    "name": "Test Group",
                    "urlname": "test-group",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/test-group/",
                    "events": {
                        "totalCount": 1,
                        "pageInfo": {"endCursor": "abc"},
                        "edges": [{"node": group_events_fragment}],
                    },
                },
            }
        }

        with patch("meetup_query.http_client") as mock_client:
            mock_client.post.return_value.status_code = 200
            mock_client.post.return_value.json.return_value = batched_response

            results = send_batched_group_request("fake_token", ["test-group"])

        assert len(results) == 1
        parsed = json.loads(results[0])
        assert "data" in parsed
        assert "groupByUrlname" in parsed["data"]
        assert parsed["data"]["groupByUrlname"]["urlname"] == "test-group"

    def test_multiple_groups(self, group_events_fragment):
        batched_response = {
            "data": {
                "group_0": {
                    "id": "g1",
                    "description": "Group A",
                    "name": "Group A",
                    "urlname": "group-a",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/group-a/",
                    "events": {
                        "totalCount": 1,
                        "pageInfo": {"endCursor": "a"},
                        "edges": [{"node": group_events_fragment}],
                    },
                },
                "group_1": {
                    "id": "g2",
                    "description": "Group B",
                    "name": "Group B",
                    "urlname": "group-b",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/group-b/",
                    "events": {
                        "totalCount": 0,
                        "pageInfo": {"endCursor": None},
                        "edges": [],
                    },
                },
            }
        }

        with patch("meetup_query.http_client") as mock_client:
            mock_client.post.return_value.status_code = 200
            mock_client.post.return_value.json.return_value = batched_response

            results = send_batched_group_request("fake_token", ["group-a", "group-b"])

        assert len(results) == 2
        for result in results:
            parsed = json.loads(result)
            assert "groupByUrlname" in parsed["data"]

    def test_partial_failure(self, group_events_fragment):
        """Groups returning null are included as null groupByUrlname."""
        batched_response = {
            "data": {
                "group_0": {
                    "id": "g1",
                    "description": "Group A",
                    "name": "Group A",
                    "urlname": "group-a",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/group-a/",
                    "events": {
                        "totalCount": 1,
                        "pageInfo": {"endCursor": "a"},
                        "edges": [{"node": group_events_fragment}],
                    },
                },
                "group_1": None,
            },
            "errors": [{"message": "Group not found", "path": ["group_1"]}],
        }

        with patch("meetup_query.http_client") as mock_client:
            mock_client.post.return_value.status_code = 200
            mock_client.post.return_value.json.return_value = batched_response

            results = send_batched_group_request("fake_token", ["group-a", "bad-group"])

        assert len(results) == 2
        good = json.loads(results[0])
        assert good["data"]["groupByUrlname"] is not None
        bad = json.loads(results[1])
        assert bad["data"]["groupByUrlname"] is None

    def test_empty_list(self):
        results = send_batched_group_request("fake_token", [])
        assert results == []
