from app.infrastructure.adapters.book_adapter import BookAdapter
from app.services.book_service import BookService
from app.usecases.stats.get_overview_stats_use_case import GetOverviewStatsUseCase
from app.schemas.stats_schema import OverviewStats


class GetOverviewStatsController:

    def call_controller(self) -> OverviewStats:
        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        use_case = GetOverviewStatsUseCase(book_service)

        result = use_case.execute()

        return OverviewStats(**result)

