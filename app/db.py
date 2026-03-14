from datetime import datetime
from decouple import config
from pathlib import Path
from pony.orm import Database, Optional, PrimaryKey, Required, db_session  # noqa: F401

APP_DIR = Path(__file__).resolve().parent

db = Database()

_initialized = False


class Schedule(db.Entity):
    _table_ = "schedule"
    id = PrimaryKey(int, auto=True)
    day = Required(str, unique=True)
    schedule_time = Required(str)
    timezone = Required(str)
    enabled = Required(bool, default=True)
    snooze_until = Optional(datetime)
    original_schedule_time = Optional(str)
    last_changed = Required(datetime, default=datetime.utcnow)


class UserInfo(db.Entity):
    username = Required(str, unique=True)
    hashed_password = Required(str)
    email = Optional(str)


def get_db_config():
    """Return SQLite bind kwargs."""
    db_path = config("DB_PATH", default="/data/meetup_bot.db")
    return {
        "provider": "sqlite",
        "filename": db_path,
        "create_db": True,
    }


def init_db():
    """Bind the shared Database instance and generate mappings.

    Safe to call multiple times; subsequent calls are no-ops.
    """
    global _initialized
    if _initialized:
        return

    db_config = get_db_config()
    db.bind(**db_config)
    db.generate_mapping(create_tables=True)

    import sqlite3

    conn = sqlite3.connect(db_config["filename"])
    conn.execute("PRAGMA journal_mode=WAL")
    conn.close()

    _initialized = True
