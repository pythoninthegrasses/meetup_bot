import os
import pytest


@pytest.mark.unit
class TestGetDbConfig:
    def test_dev_mode_returns_sqlite_config(self):
        """DEV=true should return SQLite provider config."""
        from db import get_db_config

        config = get_db_config(dev=True)
        assert config["provider"] == "sqlite"
        assert "filename" in config
        assert config["create_db"] is True

    def test_prod_mode_returns_postgres_config(self):
        """DEV=false should return PostgreSQL provider config."""
        from db import get_db_config

        config = get_db_config(dev=False)
        assert config["provider"] == "postgres"
        assert "user" in config
        assert "password" in config
        assert "host" in config
        assert "database" in config
        assert "port" in config

    def test_dev_defaults_to_false(self):
        """DEV env var unset should default to false (PostgreSQL)."""
        os.environ.pop("DEV", None)
        from db import get_db_config

        config = get_db_config()
        assert config["provider"] == "postgres"

    def test_dev_true_env_var(self):
        """DEV=true env var should yield SQLite config."""
        os.environ["DEV"] = "true"
        try:
            from db import get_db_config

            config = get_db_config()
            assert config["provider"] == "sqlite"
        finally:
            os.environ.pop("DEV", None)


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
