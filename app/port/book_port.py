from typing import Protocol

from app.domain.models.book_domain_model import Book


class IBookRepository(Protocol):

    def get_books(self) -> list[Book]: ...
