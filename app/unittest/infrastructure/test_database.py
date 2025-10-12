import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database import Database

TEST_DATABASE_URL = "sqlite:///:memory:"

def test_database_engine_creation():
    db = Database(TEST_DATABASE_URL)
    assert db.engine is not None
    assert str(db.engine.url).startswith("sqlite")

def test_database_session_creation():
    db = Database(TEST_DATABASE_URL)
    session = db.get_session()
    assert session is not None
    from sqlalchemy.orm import Session
    assert isinstance(session, Session)
    session.close()