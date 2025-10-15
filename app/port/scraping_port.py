from typing import Protocol

from app.domain.models.book_domain_model import Book


class IScrapingRepository(Protocol):

    def scraping_bulk_insert(self, books: list[Book]) -> None: ...
