from app.services.book_service import BookService


class GetOverviewStatsUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(self) -> dict:
        """Return overview statistics from the book service."""
        return self._book_service.get_overview_stats()

