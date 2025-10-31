from decimal import Decimal
from app.domain.models.book_domain_model import Book
from app.services.book_service import BookService


class GetBooksByPriceUseCase:

    def __init__(self, book_service: BookService) -> None:
        self._book_service = book_service

    def execute(self, page: int = 1, per_page: int = 10, min_price: Decimal = Decimal('0'), max_price: Decimal = Decimal('Infinity')) -> tuple[list[Book], int]:
        return self._book_service.get_books_by_price(page, per_page, min_price, max_price)
