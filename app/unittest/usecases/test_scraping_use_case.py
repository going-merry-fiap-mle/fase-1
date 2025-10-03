import unittest
from unittest.mock import create_autospec

from app.schemas.scraping_schema import ScrapingBase
from app.services.scraper_service import ScraperService
from app.usecases.scraping_use_case import ScrapingUseCase


class TestScrapingUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = create_autospec(ScraperService, instance=True)
        self.use_case = ScrapingUseCase(scraper_service=self.mock_service)

    def _make_item(
        self,
        title="Book",
        price="£10.00",
        rating=4,
        availability="In stock",
        category="Fiction",
        image="http://example.com/image.jpg",
    ):
        return ScrapingBase(
            title=title,
            price=price,
            rating=rating,
            availability=availability,
            category=category,
            image=image,
        )

    def test_execute_returns_list_from_service_unchanged(self):
        items = [self._make_item(title="A"), self._make_item(title="B")]
        self.mock_service.scrape_books.return_value = items

        result = self.use_case.execute()

        self.assertIs(result, items)

    def test_execute_calls_scrape_books_once(self):
        self.mock_service.scrape_books.return_value = []

        _ = self.use_case.execute()

        self.mock_service.scrape_books.assert_called_once_with()

    def test_execute_items_are_scrapingbase_instances(self):
        items = [self._make_item(title="C"), self._make_item(title="D")]
        self.mock_service.scrape_books.return_value = items

        result = self.use_case.execute()

        self.assertTrue(all(isinstance(x, ScrapingBase) for x in result))

    def test_execute_returns_empty_list_when_service_returns_empty(self):
        empty_list = []
        self.mock_service.scrape_books.return_value = empty_list

        result = self.use_case.execute()

        self.assertIs(result, empty_list)
        self.assertEqual(result, [])

    def test_execute_propagates_exception_from_service(self):
        self.mock_service.scrape_books.side_effect = RuntimeError("service failure")

        with self.assertRaises(RuntimeError):
            self.use_case.execute()

    def test_execute_no_caching_calls_service_on_each_invocation(self):
        first = [self._make_item(title="First")]
        second = [self._make_item(title="Second")]
        self.mock_service.scrape_books.side_effect = [first, second]

        result1 = self.use_case.execute()
        result2 = self.use_case.execute()

        self.assertIs(result1, first)
        self.assertIs(result2, second)
        self.assertEqual(self.mock_service.scrape_books.call_count, 2)
