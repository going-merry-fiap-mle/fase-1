from app.infrastructure.adapters.category_adapter import CategoryAdapter
from app.schemas.category_schema import CategoryBase
from app.schemas.pagination_schema import PaginatedResponse, PaginationMeta
from app.services.category_service import CategoryService
from app.usecases.category.get_categories_use_case import GetCategoriesUseCase


class GetCategoriesController:

    def call_controller(self, page: int = 1, per_page: int = 10) -> PaginatedResponse[CategoryBase]:
        category_adapter = CategoryAdapter()
        category_service = CategoryService(category_adapter)
        use_case = GetCategoriesUseCase(category_service)
        categories, total = use_case.execute(page, per_page)

        categories_dto = [
            CategoryBase(
                id=str(category.id),
                name=category.name,
            )
            for category in categories
        ]

        pagination_meta = PaginationMeta(
            page=page,
            per_page=per_page,
            total_items=total
        )

        return PaginatedResponse(items=categories_dto, pagination=pagination_meta)
