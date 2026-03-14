import httpx
import os
import pytest
import shutil
import socket
import subprocess
import sys
import tempfile
import time

DB_USER = "e2e_user"
DB_PASS = "e2e_pass"


def _find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


E2E_PORT = int(os.environ.get("E2E_PORT", 0)) or _find_free_port()
BASE_URL = f"http://localhost:{E2E_PORT}"


@pytest.fixture(scope="session")
def e2e_server():
    """Start a uvicorn subprocess with a temporary SQLite database for the full e2e session."""
    tmp_dir = tempfile.mkdtemp(prefix="e2e_")
    db_path = os.path.join(tmp_dir, "e2e_meetup_bot.db")

    app_dir = os.path.join(os.path.dirname(__file__), "..", "app")
    app_dir = os.path.abspath(app_dir)

    env = os.environ.copy()
    env.update(
        {
            "DB_PATH": db_path,
            "DB_USER": DB_USER,
            "DB_PASS": DB_PASS,
            "PORT": str(E2E_PORT),
            "HOST": "localhost",
            "SECRET_KEY": "e2e-test-secret-key",
            "ALGORITHM": "HS256",
            "TOKEN_EXPIRE": "30",
            "DEV": "false",
            "OVERRIDE": "true",
            "DISABLE_IP_WHITELIST": "true",
        }
    )

    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(E2E_PORT),
            "--log-level",
            "warning",
        ],
        cwd=app_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            resp = httpx.get(f"{BASE_URL}/healthz", timeout=1)
            if resp.status_code == 200:
                break
        except httpx.ConnectError:
            pass
        time.sleep(0.5)
    else:
        stdout = proc.stdout.read().decode() if proc.stdout else ""
        stderr = proc.stderr.read().decode() if proc.stderr else ""
        proc.kill()
        shutil.rmtree(tmp_dir, ignore_errors=True)
        pytest.fail(f"Server failed to start within 30s.\nstdout: {stdout}\nstderr: {stderr}")

    yield {
        "base_url": BASE_URL,
        "db_user": DB_USER,
        "db_pass": DB_PASS,
    }

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture
def session(e2e_server):
    """httpx client for e2e tests."""
    with httpx.Client() as c:
        yield c


@pytest.fixture
def base_url(e2e_server):
    return e2e_server["base_url"]


@pytest.fixture
def auth_token(e2e_server, session, base_url):
    """Authenticate against the running server and return a Bearer token."""
    resp = session.post(
        f"{base_url}/token",
        data={
            "username": e2e_server["db_user"],
            "password": e2e_server["db_pass"],
        },
    )
    assert resp.status_code == 200, f"Auth failed: {resp.text}"
    return resp.json()["access_token"]


@pytest.fixture
def auth_session(session, auth_token):
    """httpx client with Authorization header set."""
    session.headers.update({"Authorization": f"Bearer {auth_token}"})
    return session


@pytest.mark.e2e
class TestHealthCheck:
    def test_health_returns_ok(self, session, base_url):
        resp = session.get(f"{base_url}/healthz")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


@pytest.mark.e2e
class TestIndexPage:
    def test_index_returns_html(self, session, base_url):
        resp = session.get(f"{base_url}/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]


@pytest.mark.e2e
class TestAuthLoginFlow:
    def test_oauth_token_success(self, e2e_server, session, base_url):
        resp = session.post(
            f"{base_url}/token",
            data={
                "username": e2e_server["db_user"],
                "password": e2e_server["db_pass"],
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_oauth_token_wrong_password(self, e2e_server, session, base_url):
        resp = session.post(
            f"{base_url}/token",
            data={
                "username": e2e_server["db_user"],
                "password": "wrong_password",
            },
        )
        assert resp.status_code == 401

    def test_form_login_redirects_to_docs(self, e2e_server, session, base_url):
        resp = session.post(
            f"{base_url}/auth/login",
            data={
                "username": e2e_server["db_user"],
                "password": e2e_server["db_pass"],
            },
            follow_redirects=False,
        )
        assert resp.status_code == 303
        assert resp.headers["location"] == "/docs"

    def test_form_login_invalid_user(self, session, base_url):
        resp = session.post(
            f"{base_url}/auth/login",
            data={"username": "nonexistent_user", "password": "password"},
        )
        assert resp.status_code == 404

    def test_protected_endpoint_without_token(self, session, base_url):
        resp = session.get(f"{base_url}/api/events")
        assert resp.status_code == 401

    def test_protected_endpoint_with_invalid_token(self, session, base_url):
        session.headers.update({"Authorization": "Bearer invalid_token"})
        resp = session.get(f"{base_url}/api/events")
        assert resp.status_code == 401


@pytest.mark.e2e
class TestEventRetrieval:
    def test_get_events_authenticated(self, auth_session, base_url):
        resp = auth_session.get(
            f"{base_url}/api/events",
            params={"location": "Oklahoma City", "exclusions": "Tulsa"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list | dict)
        if isinstance(body, dict):
            assert "events" in body or "message" in body

    def test_get_events_no_params_uses_defaults(self, auth_session, base_url):
        resp = auth_session.get(f"{base_url}/api/events")
        assert resp.status_code == 200
