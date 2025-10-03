import unittest
from unittest.mock import MagicMock, patch

from app.controller.scraping_controller import ScrapingController


class TestScrapingController(unittest.TestCase):

    def test_call_controller_instantiates_and_executes_once(self):
        with patch(
            "app.controller.scraping_controller.WebDriverService"
        ) as MockWebDriver, patch(
            "app.controller.scraping_controller.ScraperService"
        ) as MockScraperService, patch(
            "app.controller.scraping_controller.ScrapingUseCase"
        ) as MockUseCase:

            use_case_instance = MockUseCase.return_value
            expected_result = ["book1", "book2"]
            use_case_instance.execute.return_value = expected_result

            controller = ScrapingController()
            result = controller.call_controller()

            self.assertEqual(result, expected_result)
            MockWebDriver.assert_called_once_with()
            wd_instance = MockWebDriver.return_value
            MockScraperService.assert_called_once_with(wd_instance)
            scraper_instance = MockScraperService.return_value
            MockUseCase.assert_called_once_with(scraper_instance)
            use_case_instance.execute.assert_called_once_with()

    def test_call_controller_returns_use_case_result_unchanged(self):
        with patch(
            "app.controller.scraping_controller.WebDriverService"
        ) as MockWebDriver, patch(
            "app.controller.scraping_controller.ScraperService"
        ) as MockScraperService, patch(
            "app.controller.scraping_controller.ScrapingUseCase"
        ) as MockUseCase:

            passthrough_result = [{"title": "T1"}, {"title": "T2"}]
            MockUseCase.return_value.execute.return_value = passthrough_result

            controller = ScrapingController()
            result = controller.call_controller()

            self.assertIs(result, passthrough_result)

    def test_call_controller_returns_empty_list_when_no_items(self):
        with patch("app.controller.scraping_controller.WebDriverService"), patch(
            "app.controller.scraping_controller.ScraperService"
        ), patch("app.controller.scraping_controller.ScrapingUseCase") as MockUseCase:

            MockUseCase.return_value.execute.return_value = []

            controller = ScrapingController()
            result = controller.call_controller()

            self.assertEqual(result, [])

    def test_call_controller_propagates_on_webdriver_init_failure(self):
        with patch(
            "app.controller.scraping_controller.WebDriverService",
            side_effect=RuntimeError("init failed"),
        ) as MockWebDriver, patch(
            "app.controller.scraping_controller.ScraperService"
        ) as MockScraperService, patch(
            "app.controller.scraping_controller.ScrapingUseCase"
        ) as MockUseCase:

            controller = ScrapingController()
            with self.assertRaises(RuntimeError):
                controller.call_controller()

            MockWebDriver.assert_called_once_with()
            MockScraperService.assert_not_called()
            MockUseCase.assert_not_called()

    def test_call_controller_propagates_on_use_case_execute_error(self):
        with patch(
            "app.controller.scraping_controller.WebDriverService"
        ) as MockWebDriver, patch(
            "app.controller.scraping_controller.ScraperService"
        ) as MockScraperService, patch(
            "app.controller.scraping_controller.ScrapingUseCase"
        ) as MockUseCase:

            use_case_instance = MockUseCase.return_value
            use_case_instance.execute.side_effect = ValueError("execution failed")

            controller = ScrapingController()
            with self.assertRaises(ValueError):
                controller.call_controller()

            MockWebDriver.assert_called_once_with()
            wd_instance = MockWebDriver.return_value
            MockScraperService.assert_called_once_with(wd_instance)
            scraper_instance = MockScraperService.return_value
            MockUseCase.assert_called_once_with(scraper_instance)
            use_case_instance.execute.assert_called_once_with()

    def test_call_controller_creates_new_dependencies_per_call(self):
        with patch(
            "app.controller.scraping_controller.WebDriverService"
        ) as MockWebDriver, patch(
            "app.controller.scraping_controller.ScraperService"
        ) as MockScraperService, patch(
            "app.controller.scraping_controller.ScrapingUseCase"
        ) as MockUseCase:

            wd1, wd2 = MagicMock(name="WD1"), MagicMock(name="WD2")
            sc1, sc2 = MagicMock(name="SC1"), MagicMock(name="SC2")
            uc1, uc2 = MagicMock(name="UC1"), MagicMock(name="UC2")

            MockWebDriver.side_effect = [wd1, wd2]
            MockScraperService.side_effect = [sc1, sc2]
            MockUseCase.side_effect = [uc1, uc2]

            uc1.execute.return_value = ["r1"]
            uc2.execute.return_value = ["r2"]

            controller = ScrapingController()

            res1 = controller.call_controller()
            res2 = controller.call_controller()

            self.assertEqual(res1, ["r1"])
            self.assertEqual(res2, ["r2"])

            self.assertEqual(MockWebDriver.call_count, 2)
            self.assertEqual(MockScraperService.call_count, 2)
            self.assertEqual(MockUseCase.call_count, 2)

            self.assertEqual(MockScraperService.call_args_list[0].args[0], wd1)
            self.assertEqual(MockScraperService.call_args_list[1].args[0], wd2)

            self.assertEqual(MockUseCase.call_args_list[0].args[0], sc1)
            self.assertEqual(MockUseCase.call_args_list[1].args[0], sc2)

            uc1.execute.assert_called_once_with()
            uc2.execute.assert_called_once_with()
