from app.domain.models import Book
from app.port.book_port import IBookRepository


class BookRepository(IBookRepository):

    def get_books(self) -> list[Book]:
        # aqui deve ser a query sqlalchemy para a buscar os livros no banco
        test = Book(
            title="fake",
            price="10euro",
            rating=1,
            availability="In stock",
            category="Poetry",
            image="fakeimage.jpg",
        )
        return [test]
