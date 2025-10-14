import uuid
from typing import Optional, TYPE_CHECKING, List
from decimal import Decimal
from sqlalchemy import (
    String, Integer, DECIMAL, DateTime, ForeignKey, CheckConstraint, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone
import enum
import sqlalchemy


class Base(DeclarativeBase):
    pass


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint('(rating >= 1 AND rating <= 5) OR rating IS NULL', name='check_rating_range'),
        UniqueConstraint('id', name='uq_books_id'),
        sqlalchemy.Index('ix_books_category_id', 'category_id'),
        sqlalchemy.Index('ix_books_rating', 'rating'),
        sqlalchemy.Index('ix_books_price', 'price'),
        sqlalchemy.Index('ix_books_availability', 'availability'),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    availability: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="books", lazy="select")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        sqlalchemy.Index('ix_categories_id', 'id'),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="category", lazy="select")


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)