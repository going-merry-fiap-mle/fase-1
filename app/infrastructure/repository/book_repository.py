from decimal import Decimal
from uuid import UUID

from app.domain.models.book_domain_model import Book as DomainBook
from app.infrastructure.models.book import Book
from app.infrastructure.session_manager import get_session
from app.port.book_port import IBookRepository


class BookRepository(IBookRepository):

    def get_books(self, page: int = 1, per_page: int = 10) -> tuple[list[DomainBook], int]:
        with get_session() as session:
            total = session.query(Book).count()

            offset = (page - 1) * per_page
            books_orm = (
                session.query(Book)
                .offset(offset)
                .limit(per_page)
                .all()
            )

            domain_books = [book.to_domain() for book in books_orm]

            return domain_books, total

    def create_book(
        self,
        title: str,
        price: str,
        rating: int | None,
        availability: str,
        category_id: UUID,
        image_url: str
    ) -> DomainBook:
        with get_session() as session:
            book_db = Book(
                title=title,
                price=Decimal(price.replace('£', '').replace('€', '')),
                availability=availability,
                category_id=category_id,
                image_url=image_url,
                rating=rating,
            )

            session.add(book_db)
            session.flush()

            return book_db.to_domain()


    def get_book_by_id(self, book_id : UUID) -> DomainBook | None:
        with get_session() as session:
            total = session.query(Book).count()

        book_orm = session.get(Book, book_id)

        if book_orm is None:
            return None

        domain_book = book_orm.to_domain()

        return domain_book