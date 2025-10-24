from app.services.category_service import CategoryService


class GetCategoryStatsUseCase:

    def __init__(self, category_service: CategoryService) -> None:
        self._category_service = category_service

    def execute(self, page: int = 1, per_page: int = 10) -> tuple[list[dict], int]:
        return self._category_service.get_category_stats(page, per_page)
