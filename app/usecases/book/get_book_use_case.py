from typing import Tuple

from app.domain.models import Book
from app.services.book_service import BookService


class GetBookUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(self, page: int = 1, per_page: int = 10) -> Tuple[list[Book], int]:
        return self._book_service.get_books(page, per_page)
