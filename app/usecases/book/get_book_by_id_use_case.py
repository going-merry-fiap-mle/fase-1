from app.domain.models.book_domain_model import Book
from app.services.book_service import BookService


class GetBookByIdUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(self, book_id) -> Book | None:
        return self._book_service.get_book_by_id(book_id)
