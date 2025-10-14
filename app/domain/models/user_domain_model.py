from app.infrastructure.models.enums.admin_enum import UserRole


class User:
    def __init__(self, username: str, password: str, role: UserRole) -> None:
        self.username = username
        self.password = password
        self.role = role
