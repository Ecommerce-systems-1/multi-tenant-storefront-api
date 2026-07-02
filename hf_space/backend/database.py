import sqlite3
from typing import Generator

_conn: sqlite3.Connection | None = None

def init_db(path: str = "store.db") -> sqlite3.Connection:
    global _conn
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _conn = conn
    return conn

def get_db() -> Generator[sqlite3.Connection, None, None]:
    yield _conn