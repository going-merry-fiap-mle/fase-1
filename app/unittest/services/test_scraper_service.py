import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, call, patch

from app.schemas.scraping_schema import ScrapingBase
from app.services.scraper_service import ScraperService


class TestScraperService(unittest.TestCase):
    def test_scrape_books_paginates_and_aggregates_results(self) -> None:
        driver_mock = MagicMock()
        web_driver_mock = MagicMock()
        web_driver_mock.driver = driver_mock
        web_driver_mock.url = "http://example.com/start"

        book_el_1 = MagicMock()
        book_el_2 = MagicMock()
        book_el_3 = MagicMock()

        driver_mock.find_elements.side_effect = [
            [book_el_1, book_el_2],
            [book_el_3],
        ]

        next_button = MagicMock()
        next_button.get_attribute.return_value = "http://example.com/next"
        driver_mock.find_element.side_effect = [
            next_button,
            Exception("no next"),
        ]

        parsed_1 = ScrapingBase(
            title="Title 1",
            price="£10.00",
            rating=5,
            availability="In stock",
            category="Cat1",
            image_url="img1",
        )
        parsed_2 = ScrapingBase(
            title="Title 2",
            price="£12.00",
            rating=4,
            availability="In stock",
            category="Cat2",
            image_url="img2",
        )
        parsed_3 = ScrapingBase(
            title="Title 3",
            price="£13.00",
            rating=3,
            availability="In stock",
            category="Cat3",
            image_url="img3",
        )

        with patch("app.services.scraper_service.AppLogger"):
            with patch.object(
                ScraperService,
                "_parse_book",
                side_effect=[parsed_1, parsed_2, parsed_3],
            ):
                service = ScraperService(
                    web_driver=web_driver_mock, scraping_repository=MagicMock()
                )
                results = service.scrape_books()

        self.assertEqual(len(results), 3)
        self.assertIsInstance(results[0], ScrapingBase)
        self.assertEqual([r.title for r in results], ["Title 1", "Title 2", "Title 3"])
        driver_mock.get.assert_has_calls(
            [call("http://example.com/start"), call("http://example.com/next")]
        )
        driver_mock.quit.assert_called_once()

    def test_parse_book_extracts_all_fields_with_rating_mapping(self) -> None:
        driver_mock = MagicMock()
        web_driver_mock = MagicMock()
        web_driver_mock.driver = driver_mock

        book_el = MagicMock()
        h3_el = MagicMock()
        a_el = MagicMock()
        price_el = MagicMock()
        rating_p_el = MagicMock()
        availability_el = MagicMock()
        img_el = MagicMock()

        book_el.find_element.side_effect = [
            h3_el,
            price_el,
            rating_p_el,
            availability_el,
            img_el,
        ]

        h3_el.find_element.return_value = a_el

        def a_get_attr(name):
            return {"title": "A Great Book", "href": "http://example.com/book/1"}.get(
                name
            )

        a_el.get_attribute.side_effect = a_get_attr

        price_el.text = "£51.77"
        rating_p_el.get_attribute.return_value = "star-rating Three"
        availability_el.text = " In stock (22 available) "
        img_el.get_attribute.return_value = "http://example.com/img.jpg"

        category_el = MagicMock()
        category_el.text = "Science"
        driver_mock.find_element.return_value = category_el

        with patch("app.services.scraper_service.AppLogger"):
            service = ScraperService(
                web_driver=web_driver_mock, scraping_repository=MagicMock()
            )
            result = service._parse_book(
                book_el, {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            )

        self.assertIsInstance(result, ScrapingBase)
        self.assertEqual(result.title, "A Great Book")
        self.assertEqual(result.price, "£51.77")
        self.assertEqual(result.rating, 3)
        self.assertEqual(result.availability, "In stock (22 available)")
        self.assertEqual(result.category, "Science")
        self.assertEqual(result.image_url, "http://example.com/img.jpg")

    def test_parse_book_navigates_to_detail_and_returns_to_listing(self) -> None:
        driver_mock = MagicMock()
        web_driver_mock = MagicMock()
        web_driver_mock.driver = driver_mock

        book_el = MagicMock()
        h3_el = MagicMock()
        a_el = MagicMock()
        price_el = MagicMock()
        rating_p_el = MagicMock()
        availability_el = MagicMock()
        img_el = MagicMock()
        book_el.find_element.side_effect = [
            h3_el,
            price_el,
            rating_p_el,
            availability_el,
            img_el,
        ]
        h3_el.find_element.return_value = a_el

        a_el.get_attribute.side_effect = lambda name: {
            "title": "Book A",
            "href": "http://example.com/book/A",
        }.get(name)
        price_el.text = "£10.00"
        rating_p_el.get_attribute.return_value = "star-rating Four"
        availability_el.text = " In stock "
        img_el.get_attribute.return_value = "http://example.com/a.jpg"

        category_el = MagicMock()
        category_el.text = "Classics"
        driver_mock.find_element.return_value = category_el

        with patch("app.services.scraper_service.AppLogger"):
            service = ScraperService(
                web_driver=web_driver_mock, scraping_repository=MagicMock()
            )
            _ = service._parse_book(
                book_el, {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            )

        driver_mock.get.assert_called_with("http://example.com/book/A")
        driver_mock.back.assert_called_once()

    def test_scrape_books_terminates_and_quits_when_next_absent(self) -> None:
        driver_mock = MagicMock()
        web_driver_mock = MagicMock()
        web_driver_mock.driver = driver_mock
        web_driver_mock.url = "http://example.com/start"

        book_el = MagicMock()
        driver_mock.find_elements.return_value = [book_el]
        driver_mock.find_element.side_effect = Exception("no next")

        parsed = ScrapingBase(
            title="Only Book",
            price="£5.00",
            rating=2,
            availability="In stock",
            category="Misc",
            image_url="img",
        )

        with patch("app.services.scraper_service.AppLogger") as LoggerMock:
            logger_instance = LoggerMock.return_value
            with patch.object(ScraperService, "_parse_book", return_value=parsed):
                service = ScraperService(
                    web_driver=web_driver_mock, scraping_repository=MagicMock()
                )
                results = service.scrape_books()

        self.assertEqual(len(results), 1)
        driver_mock.quit.assert_called_once()

        self.assertEqual(service.endless_loop_index, 0)

        logger_instance.info.assert_any_call(
            "Extração concluida com sucesso", HTTPStatus.CONTINUE
        )

    def test_parse_book_unrecognized_rating_defaults_to_zero(self) -> None:
        driver_mock = MagicMock()
        web_driver_mock = MagicMock()
        web_driver_mock.driver = driver_mock

        book_el = MagicMock()
        h3_el = MagicMock()
        a_el = MagicMock()
        price_el = MagicMock()
        rating_p_el = MagicMock()
        availability_el = MagicMock()
        img_el = MagicMock()
        book_el.find_element.side_effect = [
            h3_el,
            price_el,
            rating_p_el,
            availability_el,
            img_el,
        ]
        h3_el.find_element.return_value = a_el

        a_el.get_attribute.side_effect = lambda name: {
            "title": "Odd Rating Book",
            "href": "http://example.com/odd",
        }.get(name)
        price_el.text = "£9.99"
        rating_p_el.get_attribute.return_value = "star-rating Unknown"
        availability_el.text = " In stock "
        img_el.get_attribute.return_value = "http://example.com/odd.jpg"

        category_el = MagicMock()
        category_el.text = "Unknown"
        driver_mock.find_element.return_value = category_el

        with patch("app.services.scraper_service.AppLogger"):
            service = ScraperService(
                web_driver=web_driver_mock, scraping_repository=MagicMock()
            )
            result = service._parse_book(
                book_el, {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            )

        self.assertEqual(result.rating, 0)

    def test_parse_book_skips_navigation_when_book_link_missing(self) -> None:
        driver_mock = MagicMock()
        web_driver_mock = MagicMock()
        web_driver_mock.driver = driver_mock

        book_el = MagicMock()
        h3_el = MagicMock()
        a_el = MagicMock()
        price_el = MagicMock()
        rating_p_el = MagicMock()
        availability_el = MagicMock()
        img_el = MagicMock()
        book_el.find_element.side_effect = [
            h3_el,
            price_el,
            rating_p_el,
            availability_el,
            img_el,
        ]
        h3_el.find_element.return_value = a_el

        a_el.get_attribute.side_effect = lambda name: {
            "title": "No Link Book",
            "href": "",
        }.get(name)
        price_el.text = "£7.00"
        rating_p_el.get_attribute.return_value = "star-rating Two"
        availability_el.text = " In stock "
        img_el.get_attribute.return_value = "http://example.com/nolink.jpg"

        category_el = MagicMock()
        category_el.text = "General"
        driver_mock.find_element.return_value = category_el

        with patch("app.services.scraper_service.AppLogger"):
            service = ScraperService(
                web_driver=web_driver_mock, scraping_repository=MagicMock()
            )
            result = service._parse_book(
                book_el, {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            )

        driver_mock.get.assert_not_called()
        self.assertIsInstance(result, ScrapingBase)
        self.assertEqual(result.title, "No Link Book")
        self.assertEqual(result.category, "General")
