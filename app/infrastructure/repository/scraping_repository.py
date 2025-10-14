from app.domain.models.book_domain_model import Book as DomainBook
from app.infrastructure.models.book import Book
from app.infrastructure.repository.category_repository import CategoryRepository
from app.infrastructure.session_manager import get_session
from app.port.scraping_port import IScrapingRepository
from app.utils.logger import AppLogger


class ScrapingRepository(IScrapingRepository):

    def __init__(self) -> None:
        self._category_repository = CategoryRepository()
        self.logger = AppLogger("ScrapingRepository")

    def scraping_bulk_insert(self, books: list[DomainBook]) -> None:
        with get_session() as session:
            for book in books:
                category = self._category_repository.get_or_create_by_name(
                    book.category.name
                )
                book.category.id = category.id

            books_orm = [Book.from_domain(book) for book in books]

            session.bulk_save_objects(books_orm)
            session.commit()
            self.logger.info(f"Inserted {len(books)} books into the database")
