from app.services.scraper_service import ScraperService


class ScrapingUseCase:

    def __init__(self, scraper_service: ScraperService) -> None:
        self._scraping_service: ScraperService = scraper_service

    def execute(self) -> None:
        service = self._scraping_service
        scraping = service.scrape_books()
        service.save_books(scraping)
