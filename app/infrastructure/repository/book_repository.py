from typing import Optional

from app.domain.models.book_domain_model import Book as DomainBook
from app.infrastructure.models.book import Book
from app.infrastructure.session_manager import get_session
from app.port.book_port import IBookRepository


class BookRepository(IBookRepository):

    def get_books(self) -> list[DomainBook]:
        with get_session() as session:
            books_orm = session.query(Book).all()
            return [book.to_domain() for book in books_orm]  # type: ignore

    def get_book_by_id(self, book_id: str) -> Optional[DomainBook]:
        with get_session() as session:
            book_orm = session.query(Book).filter(Book.id == book_id).first()
            return book_orm.to_domain() if book_orm else None  # type: ignore
