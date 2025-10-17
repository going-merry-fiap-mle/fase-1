from uuid import UUID

from app.domain.models.book_domain_model import Book
from app.infrastructure.repository.book_repository import BookRepository
from app.port.book_port import IBookRepository


class BookAdapter(IBookRepository):

    def __init__(self) -> None:
        self._repository = BookRepository()

    def get_books(self, page: int = 1, per_page: int = 10) -> tuple[list[Book], int]:
        return self._repository.get_books(page, per_page)

    def create_book(
        self,
        title: str,
        price: str,
        rating: int | None,
        availability: str,
        category_id: UUID,
        image_url: str
    ) -> Book:
        return self._repository.create_book(
            title=title,
            price=price,
            rating=rating,
            availability=availability,
            category_id=category_id,
            image_url=image_url
        )
