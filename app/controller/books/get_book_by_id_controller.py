from app.domain.models.book_domain_model import Book
from app.infrastructure.adapters.book_adapter import BookAdapter
from app.schemas.book_schema import BookBase
from app.services.book_service import BookService
from app.usecases.book.get_book_by_id_use_case import GetBookByIdUseCase


class GetBookByIdController:

    def call_controller(self, book_id) -> BookBase | None:
        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        use_case = GetBookByIdUseCase(book_service)
        book = use_case.execute(book_id)

        if book:
            book_dto = BookBase(
                    id=str(book.id),
                    title=book.title,
                    price=str(book.price),
                    rating=book.rating if book.rating is not None else 0,
                    availability=book.availability,
                    category=book.category.name,
                    image_url=book.image_url,
                )
        else:
            return None
        return book_dto
