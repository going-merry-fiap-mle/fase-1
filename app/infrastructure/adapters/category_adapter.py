from app.domain.models import Category
from app.infrastructure.repository.category_repository import CategoryRepository
from app.port.category_port import ICategoryRepository


class CategoryAdapter(ICategoryRepository):

    def __init__(self) -> None:
        self._repository = CategoryRepository()

    def get_categories(self) -> list[Category]:
        return self._repository.get_categories()
