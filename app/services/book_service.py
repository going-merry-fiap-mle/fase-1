from app.domain.models.book_domain_model import Book
from app.port.book_port import IBookRepository


class BookService:

    def __init__(self, book_repository: IBookRepository) -> None:
        self._book_repository = book_repository

    def get_books(self) -> list[Book]:
        return self._book_repository.get_books()
