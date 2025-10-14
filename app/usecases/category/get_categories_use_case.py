from app.domain.models import Category
from app.services.category_service import CategoryService


class GetCategoriesUseCase:

    def __init__(self, category_service: CategoryService) -> None:
        self._category_service = category_service

    def execute(self) -> list[Category]:
        return self._category_service.get_categories()
