from app.port.book_port import IBookRepository
from app.domain.models import Book


class BookService:

    def __init__(self, book_repository: IBookRepository) -> None:
        self._book_repository = book_repository

    def get_books(self) -> list[Book]:
        return self._book_repository.get_books()

    def search_books(self, title: str | None = None, category: str | None = None) -> list[Book]:
        return self._book_repository.search_books(title=title, category=category)
