import math
from typing import Tuple

from app.infrastructure.adapters.book_adapter import BookAdapter
from app.schemas.book_schema import BookBase
from app.schemas.pagination_schema import PaginatedResponse, PaginationMeta
from app.services.book_service import BookService
from app.usecases.book.get_book_use_case import GetBookUseCase


class GetBookController:

    def call_controller(self, page: int = 1, per_page: int = 10) -> PaginatedResponse[BookBase]:
        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        use_case = GetBookUseCase(book_service)
        books, total = use_case.execute(page, per_page)

        books_dto = [
            BookBase(
                title=b.title,
                price=str(b.price),
                rating=b.rating if b.rating is not None else 0,
                availability=b.availability,
                category=b.category.name,
                image_url=b.image_url,
            )
            for book in books
        ]

        total_pages = math.ceil(total / per_page) if per_page > 0 else 0

        pagination_meta = PaginationMeta(
            page=page,
            per_page=per_page,
            total_items=total,
            total_pages=total_pages
        )

        return PaginatedResponse(items=books_dto, pagination=pagination_meta)
