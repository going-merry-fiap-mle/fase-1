"""
Módulo de persistência de dados.
Implemente aqui a lógica para salvar e recuperar dados do sistema.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/postgres"  # substituir pela env futuramente

class Database:
    def __init__(self, db_url: str = DATABASE_URL):
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

# Instância global para uso em toda a aplicação
db = Database()