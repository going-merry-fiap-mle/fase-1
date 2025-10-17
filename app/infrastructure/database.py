from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Self

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.utils import AppLogger, EnvironmentLoader


class Database:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._logger = AppLogger("Database")
            self._env_loader = EnvironmentLoader()
            self._db_url: str
            self._load_variables()

            engine_kwargs: dict[str, Any] = {"echo": False}
            if not self._db_url.startswith("sqlite"):
                engine_kwargs.update(
                    {
                        "pool_size": 5,
                        "max_overflow": 10,
                        "pool_recycle": 3600,
                        "pool_pre_ping": True,
                    }
                )

            self.engine = create_engine(self._db_url, **engine_kwargs)
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
        db_url = str(self._env_loader.get("DATABASE_URL", "sqlite:///:memory:"))
        # SQLAlchemy 1.4+ requires 'postgresql://' instead of 'postgres://'
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        self._db_url = db_url
