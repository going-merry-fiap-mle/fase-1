from app.domain.models.book_domain_model import Book
from app.infrastructure.repository.scraping_repository import ScrapingRepository
from app.port.scraping_port import IScrapingRepository


class ScrapingAdapter(IScrapingRepository):

    def __init__(self) -> None:
        self._repository = ScrapingRepository()

    def scraping_bulk_insert(self, books: list[Book]) -> None:
        return self._repository.scraping_bulk_insert(books)
