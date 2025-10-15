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
                price=str(b.price),
                rating=b.rating if b.rating is not None else 0,
                availability=b.availability,
                category=b.category.name,
                image_url=b.image_url,
            )
            for b in books
        ]

        return books_dto
