from app.domain.models.book_domain_model import Book
from app.services.book_service import BookService


class GetBookUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(self) -> list[Book]:
        return self._book_service.get_books()
