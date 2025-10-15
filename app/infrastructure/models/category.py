import uuid
from typing import TYPE_CHECKING, Self

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.category_domain_model import Category as DomainCategory

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .book import Book


class Category(TimestampMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (Index("ix_categories_id", "id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4, init=False)
    name: Mapped[str] = mapped_column(String, unique=True)

    books: Mapped[list["Book"]] = relationship(back_populates="category", init=False, default_factory=list)

    @classmethod
    def from_domain(cls, category: DomainCategory) -> Self:
        instance = cls(name=category.name)
        instance.id = category.id
        return instance

    def to_domain(self) -> DomainCategory:
        return DomainCategory(name=self.name, id=self.id)
