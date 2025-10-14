import uuid
from typing import Self

from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.postgresql import UUID

from app.domain.models.category_domain_model import Category as DomainCategory

from .base import Base, TimestampMixin


class Category(TimestampMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (Index("ix_categories_id", "id"),)

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name = Column(String, unique=True, nullable=False)

    @classmethod
    def from_domain(cls, category: DomainCategory) -> Self:
        return cls(id=category.id, name=category.name)  # type: ignore

    def to_domain(self) -> DomainCategory:
        return DomainCategory(name=self.name, id=self.id)  # type: ignore
