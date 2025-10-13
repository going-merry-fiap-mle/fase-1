from app.infrastructure.adapters.scraping_adapter import ScrapingAdapter
from app.infrastructure.webdriver_infrastructure import WebDriverInfrastructure
from app.services.scraper_service import ScraperService
from app.usecases.scraping_use_case import ScrapingUseCase


class ScrapingController:

    def call_controller(self) -> None:
        scraper_adapter = ScrapingAdapter()
        web_driver = WebDriverInfrastructure()
        scraper_service = ScraperService(web_driver, scraper_adapter)
        use_case = ScrapingUseCase(scraper_service)

        use_case.execute()
