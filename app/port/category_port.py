from typing import Protocol

from app.domain.models import Category


class ICategoryRepository(Protocol):

    def get_categories(self, page: int = 1, per_page: int = 10) -> tuple[list[Category], int]: ...

    def get_or_create_category(self, name: str) -> Category: ...
