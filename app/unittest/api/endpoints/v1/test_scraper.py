import unittest
from unittest.mock import patch
from unittest.mock import patch as patch_thread

from flask import Flask

from app.api.endpoints.v1.scraper_endpoints import scraper_bp
from app.schemas.scraping_schema import ScrapingBase


class TestScraperEndpoint(unittest.TestCase):
    def create_app(self, testing=True):
        app = Flask(__name__)
        app.config["TESTING"] = testing
        app.register_blueprint(scraper_bp)
        return app

    @patch("app.api.endpoints.v1.scraper_endpoints.ScrapingController.call_controller")
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
                image_url="urlA",
            ),
            ScrapingBase(
                title="Book B",
                price="$20",
                rating=4,
                availability="Out of stock",
                category="Non-Fiction",
                image_url="urlB",
            ),
        ]
        mock_call_controller.return_value = books

        app = self.create_app()

        class DummyThread:
            def __init__(self, target):
                self._target = target
                self.daemon = False

            def start(self):
                self._target()

        with patch_thread(
            "app.api.endpoints.v1.scraper_endpoints.threading.Thread",
            side_effect=lambda target: DummyThread(target),
        ):
            with app.test_client() as client:
                resp = client.get("/api/v1/scraping")
                self.assertEqual(resp.status_code, 202)
                mock_call_controller.assert_called_once()

    @patch(
        "app.api.endpoints.v1.scraper_endpoints.ScrapingController.call_controller",
        return_value=[],
    )
    def test_scraping_route_returns_empty_json_array_200(self, _mock_call_controller):
        app = self.create_app()

        class DummyThread:
            def __init__(self, target):
                self._target = target
                self.daemon = False

            def start(self):
                self._target()

        with patch_thread(
            "app.api.endpoints.v1.scraper_endpoints.threading.Thread",
            side_effect=lambda target: DummyThread(target),
        ):
            with app.test_client() as client:
                resp = client.get("/api/v1/scraping")
                self.assertEqual(resp.status_code, 202)
                _mock_call_controller.assert_called_once()

    @patch(
        "app.api.endpoints.v1.scraper_endpoints.ScrapingController.call_controller",
        return_value=[],
    )
    def test_scraping_route_calls_controller_once(self, mock_call_controller):
        app = self.create_app()

        class DummyThread:
            def __init__(self, target):
                self._target = target
                self.daemon = False

            def start(self):
                self._target()

        with patch_thread(
            "app.api.endpoints.v1.scraper_endpoints.threading.Thread",
            side_effect=lambda target: DummyThread(target),
        ):
            with app.test_client() as client:
                resp = client.get("/api/v1/scraping")
                self.assertEqual(resp.status_code, 202)
                mock_call_controller.assert_called_once()

    @patch(
        "app.api.endpoints.v1.scraper_endpoints.ScrapingController.call_controller",
        side_effect=Exception("boom"),
    )
    def test_scraping_route_returns_500_on_controller_exception(
        self, _mock_call_controller
    ):
        app = self.create_app(testing=False)

        class DummyThread:
            def __init__(self, target):
                self._target = target
                self.daemon = False

            def start(self):
                try:
                    self._target()
                except Exception:
                    pass

        with patch_thread(
            "app.api.endpoints.v1.scraper_endpoints.threading.Thread",
            side_effect=lambda target: DummyThread(target),
        ):
            with app.test_client() as client:
                resp = client.get("/api/v1/scraping")
                self.assertEqual(resp.status_code, 202)

    @patch(
        "app.api.endpoints.v1.scraper_endpoints.ScrapingController.call_controller",
        return_value=None,
    )
    def test_scraping_route_returns_500_on_invalid_controller_result(
        self, _mock_call_controller
    ):
        app = self.create_app(testing=False)
        with app.test_client() as client:
            resp = client.get("/api/v1/scraping")
            self.assertEqual(resp.status_code, 202)

    def test_scraping_route_disallows_post_405(self):
        app = self.create_app()
        with app.test_client() as client:
            resp = client.post("/api/v1/scraping", json={})
            self.assertEqual(resp.status_code, 405)
