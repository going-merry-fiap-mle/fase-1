from app.domain.models import Book
from app.services.book_service import BookService


class SearchBooksUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(self, title: str | None = None, category: str | None = None) -> list[Book]:
        return self._book_service.search_books(title=title, category=category)
