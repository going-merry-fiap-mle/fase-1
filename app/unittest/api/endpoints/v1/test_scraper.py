import unittest
from unittest.mock import patch

from flask import Flask

from app.api.endpoints.v1.scraper import scraper_bp
from app.schemas.scraping_schema import ScrapingBase


class TestScraperEndpoint(unittest.TestCase):
    def create_app(self, testing=True):
        app = Flask(__name__)
        app.config["TESTING"] = testing
        app.register_blueprint(scraper_bp)
        return app

    @patch("app.api.endpoints.v1.scraper.ScrapingController.call_controller")
    def test_scraping_route_returns_serialized_books_json_200(
        self, mock_call_controller
    ):
        books = [
            ScrapingBase(
                title="Book A",
                price="$10",
                rating=5,
                availability="In stock",
                category="Fiction",
                image="urlA",
            ),
            ScrapingBase(
                title="Book B",
                price="$20",
                rating=4,
                availability="Out of stock",
                category="Non-Fiction",
                image="urlB",
            ),
        ]
        mock_call_controller.return_value = books

        app = self.create_app()
        with app.test_client() as client:
            resp = client.get("/api/v1/scraping")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, "application/json")
            self.assertTrue(resp.is_json)
            self.assertEqual(resp.get_json(), [b.model_dump() for b in books])

    @patch(
        "app.api.endpoints.v1.scraper.ScrapingController.call_controller",
        return_value=[],
    )
    def test_scraping_route_returns_empty_json_array_200(self, _mock_call_controller):
        app = self.create_app()
        with app.test_client() as client:
            resp = client.get("/api/v1/scraping")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, "application/json")
            self.assertTrue(resp.is_json)
            self.assertEqual(resp.get_json(), [])

    @patch(
        "app.api.endpoints.v1.scraper.ScrapingController.call_controller",
        return_value=[],
    )
    def test_scraping_route_calls_controller_once(self, mock_call_controller):
        app = self.create_app()
        with app.test_client() as client:
            resp = client.get("/api/v1/scraping")
            self.assertEqual(resp.status_code, 200)
            mock_call_controller.assert_called_once()

    @patch(
        "app.api.endpoints.v1.scraper.ScrapingController.call_controller",
        side_effect=Exception("boom"),
    )
    def test_scraping_route_returns_500_on_controller_exception(
        self, _mock_call_controller
    ):
        app = self.create_app(testing=False)
        with app.test_client() as client:
            resp = client.get("/api/v1/scraping")
            self.assertEqual(resp.status_code, 500)

    @patch(
        "app.api.endpoints.v1.scraper.ScrapingController.call_controller",
        return_value=None,
    )
    def test_scraping_route_returns_500_on_invalid_controller_result(
        self, _mock_call_controller
    ):
        app = self.create_app(testing=False)
        with app.test_client() as client:
            resp = client.get("/api/v1/scraping")
            self.assertEqual(resp.status_code, 500)

    def test_scraping_route_disallows_post_405(self):
        app = self.create_app()
        with app.test_client() as client:
            resp = client.post("/api/v1/scraping", json={})
            self.assertEqual(resp.status_code, 405)
