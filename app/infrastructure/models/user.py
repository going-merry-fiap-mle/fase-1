import uuid
from typing import Self

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from app.domain.models.user_domain_model import User as DomainUser
from app.infrastructure.models.enums.admin_enum import UserRole

from .base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role"), nullable=False)

    @classmethod
    def from_domain(cls, user: DomainUser) -> Self:
        return cls(username=user.username, password=user.password, role=user.role)  # type: ignore
