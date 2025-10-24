from app.infrastructure.adapters.category_adapter import CategoryAdapter
from app.services.category_service import CategoryService
from app.usecases.stats.get_category_stats_use_case import GetCategoryStatsUseCase
from app.schemas.category_stats_schema import CategoryStats
from app.schemas.pagination_schema import PaginatedResponse, PaginationMeta


class GetCategoryStatsController:

    def call_controller(self, page: int = 1, per_page: int = 10) -> PaginatedResponse[CategoryStats]:
        category_adapter = CategoryAdapter()
        category_service = CategoryService(category_adapter)
        use_case = GetCategoryStatsUseCase(category_service)

        items, total = use_case.execute(page, per_page)

        stats_dto = [CategoryStats(**item) for item in items]

        pagination_meta = PaginationMeta(
            page=page,
            per_page=per_page,
            total_items=total,
        )

        return PaginatedResponse(items=stats_dto, pagination=pagination_meta)
