from app.domain.models.book_domain_model import Book
from app.services.book_service import BookService


class TopRatedBooksUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(
        self,
        page: int = 1,
        per_page: int = 10
    ) -> tuple[list[Book], int]:
        return self._book_service.get_top_rated_books(
            page=page,
            per_page=per_page
        )
