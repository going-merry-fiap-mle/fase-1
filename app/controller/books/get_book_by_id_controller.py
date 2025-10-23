from app.domain.models.book_domain_model import Book
from app.infrastructure.adapters.book_adapter import BookAdapter
from app.services.book_service import BookService
from app.usecases.book.get_book_by_id_use_case import GetBookByIdUseCase


class GetBookByIdController:

    def call_controller(self, book_id) -> Book | None:
        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        use_case = GetBookByIdUseCase(book_service)
        book = use_case.execute(book_id)

        return book
