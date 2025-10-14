from typing import Tuple

from app.domain.models import Category
from app.services.category_service import CategoryService


class GetCategoriesUseCase:

    def __init__(self, category_service: CategoryService) -> None:
        self._category_service = category_service

    def execute(self, page: int = 1, per_page: int = 10) -> Tuple[list[Category], int]:
        return self._category_service.get_categories(page, per_page)
