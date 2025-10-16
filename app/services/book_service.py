from uuid import UUID

from app.domain.models.book_domain_model import Book
from app.port.book_port import IBookRepository


class BookService:

    def __init__(self, book_repository: IBookRepository) -> None:
        self._book_repository = book_repository

    def get_books(self, page: int = 1, per_page: int = 10) -> tuple[list[Book], int]:
        return self._book_repository.get_books(page, per_page)

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
