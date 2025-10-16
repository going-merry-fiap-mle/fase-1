from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.orm.session import Session

from app.infrastructure.database import Database


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Database().session_scope() as session:
        yield session
