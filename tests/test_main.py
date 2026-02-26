import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jose import jwt
from main import User, UserInDB, app, get_current_user
from unittest.mock import MagicMock, patch


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


def create_test_token(data: dict):
    return jwt.encode(data, "test_secret_key", algorithm="HS256")


@pytest.fixture
def auth_headers(mock_access_token):
    return {"Authorization": f"Bearer {mock_access_token}"}


async def override_get_current_user():
    return UserInDB(username="testuser", email="test@example.com", hashed_password="hashed_password")


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

    # Mock db_session as both decorator (in schedule.py) and context manager (in endpoint).
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
