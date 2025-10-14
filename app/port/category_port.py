from typing import Protocol

from app.domain.models import Category


class ICategoryRepository(Protocol):

    def get_categories(self) -> list[Category]: ...
