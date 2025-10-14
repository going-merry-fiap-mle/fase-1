from typing import Protocol

from app.domain.models import Book


class IBookRepository(Protocol):

    def get_books(self) -> list[Book]: ...

    def search_books(self, title: str | None = None, category: str | None = None) -> list[Book]: ...
