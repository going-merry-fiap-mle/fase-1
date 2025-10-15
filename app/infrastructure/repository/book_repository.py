from typing import Optional

from app.domain.models.book_domain_model import Book as DomainBook
from app.infrastructure.models.book import Book
from app.infrastructure.session_manager import get_session
from app.port.book_port import IBookRepository


class BookRepository(IBookRepository):

    def get_books(self) -> list[Book]:
        # aqui deve ser a query sqlalchemy para a buscar os livros no banco
        test = Book(
            title="fake",
            price="10euro",
            rating=1,
            availability="In stock",
            image_url="fakeimage.jpg",
        )
        return [test]
