from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy.orm.session import Session

from app.infrastructure.database import Database


@contextmanager
def get_session() -> Generator[Session, Any, None]:
    with Database().session_scope() as session:
        yield session
