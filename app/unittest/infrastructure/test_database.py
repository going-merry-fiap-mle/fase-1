from app.infrastructure.database import Database


def test_database_engine_creation() -> None:
    db = Database()
    assert db.engine is not None
    assert str(db.engine.url)


def test_database_session_creation() -> None:
    db = Database()
    from sqlalchemy.orm import Session

    with db.session_scope() as session:
        assert session is not None
        assert isinstance(session, Session)
