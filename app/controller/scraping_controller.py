from app.schemas.scraping_schema import ScrapingBase
from app.services.scraper_service import ScraperService
from app.services.webdriver_service import WebDriverService
from app.usecases.scraping_use_case import ScrapingUseCase


class ScrapingController:

    def call_controller(self) -> list[ScrapingBase]:
        web_driver = WebDriverService()
        scraper_service = ScraperService(web_driver)
        use_case = ScrapingUseCase(scraper_service)

        result = use_case.execute()

        return result
