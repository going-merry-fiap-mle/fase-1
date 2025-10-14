from typing import Optional, Tuple
from uuid import UUID
from decimal import Decimal

from app.domain.models import Book
from app.infrastructure.database import db
from app.port.book_port import IBookRepository


class BookRepository(IBookRepository):

    def get_books(self, page: int = 1, per_page: int = 10) -> Tuple[list[Book], int]:
        session = db.get_session()
        try:
            query = session.query(Book)
            total = query.count()

            offset = (page - 1) * per_page
            books = query.offset(offset).limit(per_page).all()

            return books, total
        finally:
            session.close()

    def create_book(
        self,
        title: str,
        price: str,
        rating: Optional[int],
        availability: str,
        category_id: UUID,
        image_url: str
    ) -> Book:
        session = db.get_session()
        try:
            price_decimal = Decimal(price.replace('£', '').replace(',', ''))

            book = Book(
                title=title,
                price=price_decimal,
                rating=rating,
                availability=availability,
                category_id=category_id,
                image_url=image_url
            )
            session.add(book)
            session.commit()
            session.refresh(book)
            return book
        finally:
            session.close()
