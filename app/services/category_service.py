from app.port.category_port import ICategoryRepository
from app.domain.models import Category


class CategoryService:

    def __init__(self, category_repository: ICategoryRepository) -> None:
        self._category_repository = category_repository

    def get_categories(self) -> list[Category]:
        return self._category_repository.get_categories()
