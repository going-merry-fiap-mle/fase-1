from app.infrastructure.adapters.category_adapter import CategoryAdapter
from app.schemas.category_schema import CategoryBase
from app.services.category_service import CategoryService
from app.usecases.category.get_categories_use_case import GetCategoriesUseCase


class GetCategoriesController:

    def call_controller(self) -> list[CategoryBase]:

        category_adapter = CategoryAdapter()
        category_service = CategoryService(category_adapter)
        use_case = GetCategoriesUseCase(category_service)
        categories = use_case.execute()

        categories_dto = [
            CategoryBase(
                name=c.name,
            )
            for c in categories
        ]

        return categories_dto
