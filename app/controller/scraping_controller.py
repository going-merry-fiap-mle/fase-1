from app.infrastructure.webdriver_infrastructure import WebDriverInfrastructure
from app.schemas.scraping_schema import ScrapingBase
from app.services.scraper_service import ScraperService
from app.usecases.scraping_use_case import ScrapingUseCase


class ScrapingController:

    def call_controller(self) -> list[ScrapingBase]:
        web_driver = WebDriverInfrastructure()
        scraper_service = ScraperService(web_driver)
        use_case = ScrapingUseCase(scraper_service)

        result = use_case.execute()

        return result
