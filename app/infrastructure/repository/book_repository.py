from decimal import Decimal
from uuid import UUID
import math

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

    def get_books_by_price(self, page: int = 1, per_page: int = 10, min_price: Decimal = Decimal('0'), max_price: Decimal = Decimal('Infinity')) -> tuple[list[DomainBook], int]:
        with get_session() as session:
            filters = [Book.price >= min_price]
            if not math.isinf(max_price):
                filters.append(Book.price <= max_price)

            filtered_query = session.query(Book).filter(*filters)
            total = filtered_query.count()

            offset = (page - 1) * per_page
            books_orm = (
                filtered_query
                .offset(offset)
                .limit(per_page)
                .all()
            )

            domain_books = [book.to_domain() for book in books_orm]

            return domain_books, total