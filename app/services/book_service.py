from decimal import Decimal
from uuid import UUID

from app.domain.models.book_domain_model import Book
from app.port.book_port import IBookRepository


class BookService:

    def __init__(self, book_repository: IBookRepository) -> None:
        self._book_repository = book_repository

    def get_books(self, page: int = 1, per_page: int = 10) -> tuple[list[Book], int]:
        return self._book_repository.get_books(page, per_page)

    def search_books(
        self,
        title: str | None = None,
        category: str | None = None,
        page: int = 1,
        per_page: int = 10
    ) -> tuple[list[Book], int]:
        return self._book_repository.search_books(
            title=title,
            category=category,
            page=page,
            per_page=per_page
        )

    def get_top_rated_books(
        self,
        page: int = 1,
        per_page: int = 10
    ) -> tuple[list[Book], int]:
        return self._book_repository.get_top_rated_books(
            page=page,
            per_page=per_page
        )

    def create_book(
        self,
        title: str,
        price: str,
        rating: int | None,
        availability: str,
        category_id: UUID,
        image_url: str
    ) -> Book:
        return self._book_repository.create_book(
            title=title,
            price=price,
            rating=rating,
            availability=availability,
            category_id=category_id,
            image_url=image_url
        )

    def get_books_by_price(self, page: int = 1, per_page: int = 10, min_price: Decimal = Decimal('0'), max_price: Decimal = Decimal('Infinity')) -> tuple[list[Book], int]:
        return self._book_repository.get_books_by_price(page, per_page, min_price, max_price)
          
    def get_overview_stats(self) -> dict:
        return self._book_repository.get_overview_stats()
