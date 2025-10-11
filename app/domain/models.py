from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    availability = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)