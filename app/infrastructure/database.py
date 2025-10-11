"""
Módulo de persistência de dados.
Implemente aqui a lógica para salvar e recuperar dados do sistema.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/postgres" #substituir pela env futuramente

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)