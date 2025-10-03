from app.schemas.scraping_schema import ScrapingBase
from app.services.scraper_service import ScraperService


class ScrapingUseCase:

    def __init__(self, scraper_service: ScraperService) -> None:
        self._scraping_service: ScraperService = scraper_service

    def execute(self) -> list[ScrapingBase]:
        service = self._scraping_service
        scraping = service.scrape_books()
        return scraping
