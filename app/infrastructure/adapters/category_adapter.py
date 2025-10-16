from app.domain.models import Category
from app.infrastructure.repository.category_repository import CategoryRepository
from app.port.category_port import ICategoryRepository


class CategoryAdapter(ICategoryRepository):

    def __init__(self) -> None:
        self._repository = CategoryRepository()

    def get_categories(self, page: int = 1, per_page: int = 10) -> tuple[list[Category], int]:
        return self._repository.get_categories(page, per_page)

    def get_or_create_category(self, name: str) -> Category:
        return self._repository.get_or_create_category(name)
