from app.infrastructure.database import Database


def test_database_engine_creation() -> None:
    db = Database()
    assert db.engine is not None
    assert str(db.engine.url).startswith("sqlite")


def test_database_session_creation() -> None:
    db = Database()
    session = db.session_scope()
    assert session is not None
    from sqlalchemy.orm import Session

    assert isinstance(session, Session)
    session.close()
