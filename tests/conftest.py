import os
import pony.orm
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Get the path to the root directory of the project
root_path = Path(__file__).resolve().parents[1]
app_path = root_path / "app"

# App modules use relative file paths (channels.csv, resources/templates, etc.)
# expecting cwd to be app/. pythonpath in pyproject.toml handles imports,
# but chdir is still required for filesystem I/O with relative paths.
os.chdir(app_path)

# Prevent module-level DB connection during test collection.
# schedule.py calls db.bind() and db.generate_mapping() at import time,
# which fails without a live PostgreSQL server.
pony.orm.Database.bind = lambda *a, **kw: None
pony.orm.Database.generate_mapping = lambda *a, **kw: None

# Set the path for groups.csv
groups_csv_path = app_path / "groups.csv"


@pytest.fixture
def groups_csv_fixture():
    return str(groups_csv_path)


@pytest.fixture
def mock_db():
    """Patch pony.orm db_session to be a no-op."""
    with patch("pony.orm.db_session", lambda f: f):
        yield


@pytest.fixture
def mock_slack_client():
    """Patch slack_sdk WebClient with a MagicMock."""
    mock_client = MagicMock()
    with patch("slack_sdk.WebClient", return_value=mock_client):
        yield mock_client


@pytest.fixture
def mock_meetup_api():
    """Patch requests.post for Meetup GraphQL calls."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}
        yield mock_post


@pytest.fixture
def mock_env():
    """Patch decouple.config to return test defaults."""
    defaults = {
        "SECRET_KEY": "test_secret_key",
        "URL": "http://localhost",
        "PORT": "3000",
        "SLACK_BOT_TOKEN": "xoxb-test-token",
        "MEETUP_API_KEY": "test-meetup-key",
    }
    with patch("decouple.config", side_effect=lambda key, **kwargs: defaults.get(key, kwargs.get("default", ""))):
        yield defaults
