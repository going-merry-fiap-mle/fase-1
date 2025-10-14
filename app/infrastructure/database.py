import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()


class Database:
    def __init__(self, db_url: str = None):
        if db_url is None:
            db_url = os.getenv(
                "DATABASE_URL",
                "postgresql+psycopg2://postgres:admin@localhost:5432/postgres"
            )
        if db_url and db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()


db = Database()