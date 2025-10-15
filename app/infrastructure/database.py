from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.utils import AppLogger, EnvironmentLoader


class Database:
    def __init__(self) -> None:
        self._logger = AppLogger("Database")

        self._env_loader = EnvironmentLoader()
        self._db_url: str
        self._load_variables()

        self.engine = create_engine(self._db_url, echo=False)
        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            self._logger.error(f"Erro ao gerenciar sessão: {str(e)}")
            raise
        finally:
            session.close()

    def _load_variables(self) -> None:
        self._db_url = self._env_loader.get("DATABASE_URL", "sqlite:///:memory:")
