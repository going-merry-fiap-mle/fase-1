import uuid
from typing import Self

from sqlalchemy import (
    DECIMAL,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.domain.models.book_domain_model import Book as DomainBook

from .base import Base, TimestampMixin


class Book(TimestampMixin, Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint(
            "(rating >= 1 AND rating <= 5) OR rating IS NULL", name="check_rating_range"
        ),
        UniqueConstraint("id", name="uq_books_id"),
        Index("ix_books_category_id", "category_id"),
        Index("ix_books_rating", "rating"),
        Index("ix_books_price", "price"),
        Index("ix_books_availability", "availability"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    title = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    rating = Column(Integer, nullable=True)
    availability = Column(String, nullable=False)
    category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    image_url = Column(String, nullable=False)

    category = relationship("Category", backref="books")

    @classmethod
    def from_domain(cls, book: DomainBook) -> Self:
        return cls(
            id=book.id,  # type: ignore
            title=book.title,  # type: ignore
            price=book.price,  # type: ignore
            rating=book.rating,  # type: ignore
            availability=book.availability,  # type: ignore
            category_id=book.category.id,  # type: ignore
            image_url=book.image_url,  # type: ignore
        )

    def to_domain(self) -> DomainBook:
        from app.domain.models.category_domain_model import Category as DomainCategory

        return DomainBook(
            id=self.id,  # type: ignore
            title=self.title,  # type: ignore
            price=self.price,  # type: ignore
            rating=self.rating,  # type: ignore
            availability=self.availability,  # type: ignore
            category=DomainCategory(name=self.category.name, id=self.category.id),  # type: ignore
            image_url=self.image_url,  # type: ignore
        )
