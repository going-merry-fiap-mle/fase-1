from app.domain.models.book_domain_model import Book
from app.infrastructure.repository.book_repository import BookRepository
from app.port.book_port import IBookRepository


class BookAdapter(IBookRepository):

    def __init__(self) -> None:
        self._repository = BookRepository()

    def get_books(self) -> list[Book]:
        return self._repository.get_books()
