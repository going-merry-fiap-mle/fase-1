import uuid
from typing import Self

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.models.user_domain_model import User as DomainUser, UserRole

from .base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4, init=False)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"))

    @classmethod
    def from_domain(cls, user: DomainUser) -> Self:
        return cls(username=user.username, password=user.password, role=user.role)
