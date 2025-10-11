from app.domain.models import Book
from app.port.book_port import IBookRepository


class BookRepository(IBookRepository):

    def get_books(self) -> list[Book]:
        # aqui deve ser a query sqlalchemy para a buscar os livros no banco
        # Exemplo: session.query(Book).all()
        # Por enquanto, retornando dados mock
        all_books = [
            Book(
                title="Python Programming",
                price="29.99",
                rating=5,
                availability="In stock",
                category="Programming",
                image="python.jpg",
            ),
            Book(
                title="Poetry Collection",
                price="15.50",
                rating=4,
                availability="In stock",
                category="Poetry",
                image="poetry.jpg",
            ),
            Book(
                title="Science Fiction Novel",
                price="19.99",
                rating=3,
                availability="In stock",
                category="Fiction",
                image="scifi.jpg",
            ),
        ]
        return all_books

    def search_books(self, title: str | None = None, category: str | None = None) -> list[Book]:
        # aqui deve ser a query sqlalchemy com filtros WHERE
        # Exemplo: session.query(Book).filter(Book.title.ilike(f'%{title}%')).filter(Book.category == category).all()
        # Por enquanto, retornando dados mock filtrados
        all_books = [
            Book(
                title="Python Programming",
                price="29.99",
                rating=5,
                availability="In stock",
                category="Programming",
                image="python.jpg",
            ),
            Book(
                title="Poetry Collection",
                price="15.50",
                rating=4,
                availability="In stock",
                category="Poetry",
                image="poetry.jpg",
            ),
            Book(
                title="Science Fiction Novel",
                price="19.99",
                rating=3,
                availability="In stock",
                category="Fiction",
                image="scifi.jpg",
            ),
        ]

        # Filtragem em memória (será substituída por query SQL)
        results = all_books

        if title:
            results = [b for b in results if title.lower() in b.title.lower()]

        if category:
            results = [b for b in results if category.lower() == b.category.lower()]

        return results
