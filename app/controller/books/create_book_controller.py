from typing import Optional

from app.infrastructure.adapters.book_adapter import BookAdapter
from app.infrastructure.adapters.category_adapter import CategoryAdapter
from app.schemas.book_schema import BookBase
from app.services.book_service import BookService
from app.services.category_service import CategoryService
from app.usecases.book.create_book_use_case import CreateBookUseCase


class CreateBookController:

    def call_controller(
        self,
        title: str,
        price: str,
        rating: Optional[int],
        availability: str,
        category_name: str,
        image_url: str
    ) -> BookBase:
        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)

        category_adapter = CategoryAdapter()
        category_service = CategoryService(category_adapter)

        use_case = CreateBookUseCase(book_service, category_service)

        book = use_case.execute(
            title=title,
            price=price,
            rating=rating,
            availability=availability,
            category_name=category_name,
            image_url=image_url
        )

        book_dto = BookBase(
            id=str(book.id),
            title=book.title,
            price=str(book.price),
            rating=book.rating,
            availability=book.availability,
            category=category_name,
            image_url=book.image_url,
        )

        return book_dto
