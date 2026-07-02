import pytest
import sqlite3
from fastapi.testclient import TestClient
from app.main import create_app
from app.database import get_db
from app.data.seed import seed_database

@pytest.fixture(scope="session")
def db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    seed_database(conn)
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def client(db):
    app = create_app(db)
    with TestClient(app) as c:
        yield c

@pytest.fixture
def styleseek_headers():
    return {"X-Tenant-ID": "styleseek"}

@pytest.fixture
def urbankicks_headers():
    return {"X-Tenant-ID": "urbankicks"}

@pytest.fixture
def luxehome_headers():
    return {"X-Tenant-ID": "luxehome"}

@pytest.fixture
def styleseek_admin_headers():
    return {"X-Tenant-ID": "styleseek", "X-Admin-Key": "styleseek-admin"}