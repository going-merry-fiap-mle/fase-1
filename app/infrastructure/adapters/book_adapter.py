from app.domain.models import Book
from app.infrastructure.repository.book_repository import BookRepository
from app.port.book_port import IBookRepository


class BookAdapter(IBookRepository):

    def __init__(self) -> None:
        self._repository = BookRepository()

    def get_books(self) -> list[Book]:
        return self._repository.get_books()

    def search_books(self, title: str | None = None, category: str | None = None) -> list[Book]:
        return self._repository.search_books(title=title, category=category)
