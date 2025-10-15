import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Self

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.book_domain_model import Book as DomainBook

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .category import Category


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

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4, init=False)
    title: Mapped[str]
    price: Mapped[Decimal]
    availability: Mapped[str]
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"))
    image_url: Mapped[str]
    rating: Mapped[int | None] = mapped_column(default=None)

    category: Mapped["Category"] = relationship(back_populates="books", init=False)

    @classmethod
    def from_domain(cls, book: DomainBook) -> Self:
        instance = cls(
            title=book.title,
            price=book.price,
            availability=book.availability,
            category_id=book.category.id,
            image_url=book.image_url,
            rating=book.rating,
        )
        instance.id = book.id
        return instance

    def to_domain(self) -> DomainBook:
        from app.domain.models.category_domain_model import Category as DomainCategory

        return DomainBook(
            id=self.id,
            title=self.title,
            price=self.price,
            rating=self.rating,
            availability=self.availability,
            category=DomainCategory(name=self.category.name, id=self.category.id),
            image_url=self.image_url,
        )
