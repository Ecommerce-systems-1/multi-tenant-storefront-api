import os
import sqlite3
from typing import Generator

_conn: sqlite3.Connection | None = None

def init_db(path: str | None = None) -> sqlite3.Connection:
    global _conn
    path = path or os.getenv("DB_PATH", "store.db")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _conn = conn
    return conn

def get_db() -> Generator[sqlite3.Connection, None, None]:
    yield _conn