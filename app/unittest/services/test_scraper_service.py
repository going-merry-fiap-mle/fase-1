import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, call, patch

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app.schemas.scraping_schema import ScrapingBase
from app.services.scraper_service import ScraperService
from app.services.webdriver_service import WebDriverService


class TestScraperService(unittest.TestCase):
    def _build_book_element(
        self,
        title="Sample Book",
        href="http://example.com/book-detail",
        price_text="£10.00",
        rating_class="star-rating Three",
        availability_text=" In stock",
        img_src="http://example.com/image.jpg",
    ):
        book_el = MagicMock(spec=WebElement)

        mock_h3 = MagicMock(spec=WebElement)
        mock_a = MagicMock(spec=WebElement)
        mock_price = MagicMock(spec=WebElement)
        mock_rating = MagicMock(spec=WebElement)
        mock_availability = MagicMock(spec=WebElement)
        mock_img = MagicMock(spec=WebElement)

        mock_a.get_attribute.side_effect = lambda attr: (
            title if attr == "title" else (href if attr == "href" else None)
        )
        mock_h3.find_element.side_effect = lambda by, val: (
            mock_a if (by == By.TAG_NAME and val == "a") else None
        )
        mock_price.text = price_text
        mock_rating.get_attribute.side_effect = lambda attr: (
            rating_class if attr == "class" else None
        )
        mock_availability.text = availability_text
        mock_img.get_attribute.side_effect = lambda attr: (
            img_src if attr == "src" else None
        )

        def book_find_element(by, val):
            if by == By.TAG_NAME and val == "h3":
                return mock_h3
            if by == By.CLASS_NAME and val == "price_color":
                return mock_price
            if by == By.CSS_SELECTOR and val == "p.star-rating":
                return mock_rating
            if by == By.CSS_SELECTOR and val == "p.instock.availability":
                return mock_availability
            if by == By.TAG_NAME and val == "img":
                return mock_img
            raise AssertionError(f"Unexpected find_element call: by={by}, val={val}")

        book_el.find_element.side_effect = book_find_element
        return book_el

    @patch("app.services.scraper_service.Logger")
    def test_scrape_books_paginates_until_no_next_and_logs_and_quits(self, MockLogger):
        web_driver = MagicMock(spec=WebDriverService)
        driver = MagicMock()
        web_driver.driver = driver
        web_driver.url = "http://site"

        book_elements = [MagicMock(spec=WebElement), MagicMock(spec=WebElement)]
        driver.find_elements.return_value = book_elements

        next_button_1 = MagicMock()
        next_button_1.get_attribute.return_value = "http://site/page-2"
        next_button_2 = MagicMock()
        next_button_2.get_attribute.return_value = "http://site/page-3"
        driver.find_element.side_effect = [
            next_button_1,
            next_button_2,
            Exception("no next"),
        ]

        service = ScraperService(web_driver)
        counter = {"i": 0}

        def parse_side_effect(book_el, rating_map):
            i = counter["i"]
            counter["i"] += 1
            return ScrapingBase(
                title=f"T{i}",
                price="£1.00",
                rating=5,
                availability="In stock",
                category="Travel",
                image=f"http://img/{i}.jpg",
            )

        with patch.object(ScraperService, "_parse_book", side_effect=parse_side_effect):
            results = service.scrape_books()

        self.assertEqual(len(results), 6)

        logger_instance = MockLogger.return_value
        logger_instance.log_info.assert_any_call(
            "Extraindo livros...", HTTPStatus.CONTINUE
        )
        logger_instance.log_info.assert_any_call(
            "Extração concluida com sucesso", HTTPStatus.CONTINUE
        )

        self.assertEqual(
            driver.get.call_args_list,
            [
                call("http://site"),
                call("http://site/page-2"),
                call("http://site/page-3"),
            ],
        )
        driver.quit.assert_called_once()

    def test_parse_book_extracts_complete_fields_and_maps_rating(self):
        web_driver = MagicMock(spec=WebDriverService)
        driver = MagicMock()
        web_driver.driver = driver

        category_el = MagicMock(spec=WebElement)
        category_el.text = "Travel"
        driver.find_element.side_effect = lambda by, val: (
            category_el
            if (by == By.CSS_SELECTOR and val == "ul.breadcrumb li:nth-child(3) a")
            else None
        )

        book_el = self._build_book_element(
            title="Book A",
            href="http://example.com/detail-a",
            price_text="£51.77",
            rating_class="star-rating Three",
            availability_text="  In stock  \n",
            img_src="http://example.com/a.jpg",
        )
        service = ScraperService(web_driver)
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

        result = service._parse_book(book_el, rating_map)

        self.assertIsInstance(result, ScrapingBase)
        self.assertEqual(result.title, "Book A")
        self.assertEqual(result.price, "£51.77")
        self.assertEqual(result.rating, 3)
        self.assertEqual(result.availability, "In stock")
        self.assertEqual(result.category, "Travel")
        self.assertEqual(result.image, "http://example.com/a.jpg")
        driver.get.assert_called_with("http://example.com/detail-a")
        driver.back.assert_called_once()

    def test_parse_book_navigates_to_detail_and_returns_to_listing(self):
        web_driver = MagicMock(spec=WebDriverService)
        driver = MagicMock()
        web_driver.driver = driver

        category_el = MagicMock(spec=WebElement)
        category_el.text = "Classics"
        driver.find_element.side_effect = lambda by, val: (
            category_el
            if (by == By.CSS_SELECTOR and val == "ul.breadcrumb li:nth-child(3) a")
            else None
        )

        book_el = self._build_book_element(
            title="Book B",
            href="http://example.com/detail-b",
            price_text="£20.00",
            rating_class="star-rating Four",
            availability_text="In stock",
            img_src="http://example.com/b.jpg",
        )
        service = ScraperService(web_driver)
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

        _ = service._parse_book(book_el, rating_map)

        driver.get.assert_called_with("http://example.com/detail-b")
        driver.back.assert_called_once()

    def test_parse_book_unknown_rating_maps_to_zero(self):
        web_driver = MagicMock(spec=WebDriverService)
        driver = MagicMock()
        web_driver.driver = driver

        category_el = MagicMock(spec=WebElement)
        category_el.text = "Mystery"
        driver.find_element.side_effect = lambda by, val: (
            category_el
            if (by == By.CSS_SELECTOR and val == "ul.breadcrumb li:nth-child(3) a")
            else None
        )

        book_el = self._build_book_element(
            title="Unknown Rating Book",
            href="http://example.com/detail-unknown",
            price_text="£15.00",
            rating_class="star-rating Zero",
            availability_text="In stock",
            img_src="http://example.com/u.jpg",
        )
        service = ScraperService(web_driver)
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

        result = service._parse_book(book_el, rating_map)

        self.assertEqual(result.rating, 0)
        driver.get.assert_called_with("http://example.com/detail-unknown")
        driver.back.assert_called_once()

    @patch("app.services.scraper_service.Logger")
    def test_scrape_books_terminates_when_next_button_missing_and_quits_driver(
        self, MockLogger
    ):
        web_driver = MagicMock(spec=WebDriverService)
        driver = MagicMock()
        web_driver.driver = driver
        web_driver.url = "http://site"

        book_elements = [MagicMock(spec=WebElement)]
        driver.find_elements.return_value = book_elements
        driver.find_element.side_effect = Exception("no next")

        service = ScraperService(web_driver)

        with patch.object(
            ScraperService,
            "_parse_book",
            return_value=ScrapingBase(
                title="Only Book",
                price="£9.99",
                rating=4,
                availability="In stock",
                category="Fiction",
                image="http://img/only.jpg",
            ),
        ):
            results = service.scrape_books()

        self.assertEqual(len(results), 1)
        logger_instance = MockLogger.return_value
        logger_instance.log_info.assert_any_call(
            "Extração concluida com sucesso", HTTPStatus.CONTINUE
        )
        driver.quit.assert_called_once()
        driver.get.assert_called_once_with("http://site")

    def test_parse_book_skips_detail_when_book_link_missing_and_continues(self):
        web_driver = MagicMock(spec=WebDriverService)
        driver = MagicMock()
        web_driver.driver = driver

        category_el = MagicMock(spec=WebElement)
        category_el.text = "General"
        driver.find_element.side_effect = lambda by, val: (
            category_el
            if (by == By.CSS_SELECTOR and val == "ul.breadcrumb li:nth-child(3) a")
            else None
        )

        book_el = self._build_book_element(
            title="No Link Book",
            href=None,
            price_text="£5.00",
            rating_class="star-rating One",
            availability_text="  In stock",
            img_src="http://example.com/nolink.jpg",
        )
        service = ScraperService(web_driver)
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

        result = service._parse_book(book_el, rating_map)

        driver.get.assert_not_called()
        driver.back.assert_called_once()

        self.assertEqual(result.title, "No Link Book")
        self.assertEqual(result.category, "General")
        self.assertEqual(result.image, "http://example.com/nolink.jpg")
