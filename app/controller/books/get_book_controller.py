from app.infrastructure.adapters.book_adapter import BookAdapter
from app.schemas.book_schema import BookBase
from app.services.book_service import BookService
from app.usecases.book.get_book_use_case import GetBookUseCase


class GetBookController:

    def call_controller(self) -> list[BookBase]:

        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        use_case = GetBookUseCase(book_service)
        books = use_case.execute()

        books_dto = [
            BookBase(
                title=b.title,
                price=b.price,
                rating=b.rating,
                availability=b.availability,
                category=str(b.category_id),
                image_url=b.image_url,
            )
            for b in books
        ]

        return books_dto
