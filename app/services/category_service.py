from typing import Tuple

from app.port.category_port import ICategoryRepository
from app.domain.models import Category


class CategoryService:

    def __init__(self, category_repository: ICategoryRepository) -> None:
        self._category_repository = category_repository

    def get_categories(self, page: int = 1, per_page: int = 10) -> Tuple[list[Category], int]:
        return self._category_repository.get_categories(page, per_page)

    def get_or_create_category(self, name: str) -> Category:
        return self._category_repository.get_or_create_category(name)
