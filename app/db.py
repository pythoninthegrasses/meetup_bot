from decouple import config
from pony.orm import Database, db_session  # noqa: F401

db = Database()

_initialized = False


def get_db_config(dev=None):
    """Return provider-specific bind kwargs based on DEV env var."""
    if dev is None:
        dev = config("DEV", default="false").lower() in ("true", "1", "yes")

    if dev:
        return {
            "provider": "sqlite",
            "filename": "db.sqlite",
            "create_db": True,
        }

    return {
        "provider": "postgres",
        "user": config("DB_USER"),
        "password": config("DB_PASS").strip('"'),
        "host": config("DB_HOST"),
        "database": config("DB_NAME"),
        "port": config("DB_PORT", default=5432, cast=int),
        "sslmode": config("DB_SSLMODE", default="prefer"),
    }


def init_db(dev=None):
    """Bind the shared Database instance and generate mappings.

    Safe to call multiple times; subsequent calls are no-ops.
    """
    global _initialized
    if _initialized:
        return

    db_config = get_db_config(dev=dev)
    db.bind(**db_config)
    db.generate_mapping(create_tables=True)
    _initialized = True
