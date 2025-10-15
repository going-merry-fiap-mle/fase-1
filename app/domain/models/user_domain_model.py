import enum


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"


class User:
    def __init__(self, username: str, password: str, role: UserRole) -> None:
        self.username = username
        self.password = password
        self.role = role
