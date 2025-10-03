from http import HTTPStatus

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.schemas.scraping_schema import ScrapingBase
from app.services.webdriver_service import WebDriverService
from app.utils.logger import Logger


class ScraperService:

    def __init__(self, web_driver: WebDriverService) -> None:
        self.web_driver = web_driver
        self.logger = Logger("ScraperService")
        self.endless_loop_index: int = -1

    def scrape_books(self) -> list[ScrapingBase]:
        books_data: list[ScrapingBase] = []
        rating_map: dict[str, int] = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }

        self.logger.log_info("Extraindo livros...", HTTPStatus.CONTINUE)

        self.web_driver.driver.get(self.web_driver.url)

        while self.endless_loop_index != 0:
            books = self.web_driver.driver.find_elements(
                By.CSS_SELECTOR, "article.product_pod"
            )

            for book in books:
                book_data = self._parse_book(book, rating_map)
                books_data.append(book_data)

            try:
                next_button = self.web_driver.driver.find_element(
                    By.CSS_SELECTOR, "li.next > a"
                )
                next_page_url = next_button.get_attribute("href")
                if next_page_url:
                    self.web_driver.driver.get(next_page_url)
            except Exception:
                self.logger.log_info(
                    "Extração concluida com sucesso", HTTPStatus.CONTINUE
                )
                self.endless_loop_index = 0
                self.web_driver.driver.quit()

        return books_data

    def _parse_book(
        self, book_element: WebElement, rating_map: dict[str, int]
    ) -> ScrapingBase:
        h3_a = book_element.find_element(By.TAG_NAME, "h3").find_element(
            By.TAG_NAME, "a"
        )
        title = h3_a.get_attribute("title")
        book_link = h3_a.get_attribute("href")

        price = book_element.find_element(By.CLASS_NAME, "price_color").text

        rating_str = (
            book_element.find_element(By.CSS_SELECTOR, "p.star-rating")
            .get_attribute("class")
            .replace("star-rating", "")
            .strip()
        )
        rating = rating_map.get(rating_str, 0)

        availability = book_element.find_element(
            By.CSS_SELECTOR, "p.instock.availability"
        ).text.strip()

        img_url = book_element.find_element(By.TAG_NAME, "img").get_attribute("src")

        if book_link:
            self.web_driver.driver.get(book_link)

        category = self.web_driver.driver.find_element(
            By.CSS_SELECTOR, "ul.breadcrumb li:nth-child(3) a"
        ).text
        self.web_driver.driver.back()

        return ScrapingBase(
            title=title,
            price=price,
            rating=rating,
            availability=availability,
            category=category,
            image=img_url,
        )
