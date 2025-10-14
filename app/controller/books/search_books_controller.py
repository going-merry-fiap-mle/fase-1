from app.infrastructure.adapters.book_adapter import BookAdapter
from app.schemas.book_schema import BookBase
from app.services.book_service import BookService
from app.usecases.book.search_books_use_case import SearchBooksUseCase


class SearchBooksController:

    def call_controller(self, title: str | None = None, category: str | None = None) -> list[BookBase]:

        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        use_case = SearchBooksUseCase(book_service)
        books = use_case.execute(title=title, category=category)

        books_dto = [
            BookBase(
                title=b.title,
                price=b.price,
                rating=b.rating,
                availability=b.availability,
                category=b.category,
                image=b.image,
            )
            for b in books
        ]

        return books_dto
