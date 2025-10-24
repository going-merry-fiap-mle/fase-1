from app.domain.models.book_domain_model import Book
from app.services.book_service import BookService


class SearchBooksUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(
        self,
        title: str | None = None,
        category: str | None = None,
        page: int = 1,
        per_page: int = 10
    ) -> tuple[list[Book], int]:
        return self._book_service.search_books(
            title=title,
            category=category,
            page=page,
            per_page=per_page
        )
