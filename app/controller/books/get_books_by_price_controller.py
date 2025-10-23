from decimal import Decimal
from app.infrastructure.adapters.book_adapter import BookAdapter
from app.schemas.book_schema import BookBase
from app.schemas.pagination_schema import PaginatedResponse, PaginationMeta
from app.services.book_service import BookService
from app.usecases.book.get_books_by_price_use_case import GetBooksByPriceUseCase


class GetBooksByPriceController:

    def call_controller(self, page: int = 1, per_page: int = 10, min_price: Decimal = Decimal('0'), max_price: Decimal = Decimal('Infinity')) -> PaginatedResponse[BookBase]:
        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        use_case = GetBooksByPriceUseCase(book_service)
        books, total = use_case.execute(page, per_page, min_price, max_price)

        books_dto = [
            BookBase(
                id=str(book.id),
                title=book.title,
                price=str(book.price),
                rating=book.rating if book.rating is not None else 0,
                availability=book.availability,
                category=book.category.name,
                image_url=book.image_url,
            )
            for book in books
        ]

        pagination_meta = PaginationMeta(
            page=page,
            per_page=per_page,
            total_items=total
        )

        return PaginatedResponse(items=books_dto, pagination=pagination_meta)
