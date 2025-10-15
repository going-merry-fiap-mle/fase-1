from typing import Protocol, Optional, Tuple
from uuid import UUID

from app.domain.models.book_domain_model import Book


class IBookRepository(Protocol):

    def get_books(self, page: int = 1, per_page: int = 10) -> Tuple[list[Book], int]: ...

    def create_book(
        self,
        title: str,
        price: str,
        rating: Optional[int],
        availability: str,
        category_id: UUID,
        image_url: str
    ) -> Book: ...
