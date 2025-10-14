from typing import Optional

from app.domain.models import Book
from app.services.book_service import BookService
from app.services.category_service import CategoryService


class CreateBookUseCase:

    def __init__(
        self,
        book_service: BookService,
        category_service: CategoryService
    ) -> None:
        self._book_service = book_service
        self._category_service = category_service

    def execute(
        self,
        title: str,
        price: str,
        rating: Optional[int],
        availability: str,
        category_name: str,
        image_url: str
    ) -> Book:
        category = self._category_service.get_or_create_category(category_name)

        book = self._book_service.create_book(
            title=title,
            price=price,
            rating=rating,
            availability=availability,
            category_id=category.id,
            image_url=image_url
        )

        return book
