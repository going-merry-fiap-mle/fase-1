import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, call, patch

from app.services.webdriver_service import WebDriverService
from app.utils.logger import Logger


class TestWebDriverService(unittest.TestCase):
    def test_init_dev_creates_firefox_without_headless_and_logs(self):
        with patch(
            "app.services.webdriver_service.EnvVariablesLoader.load_variable",
            return_value="dev",
        ) as mock_load_var, patch(
            "app.services.webdriver_service.Logger.log_info"
        ) as mock_log_info, patch(
            "app.services.webdriver_service.webdriver.FirefoxOptions"
        ) as mock_firefox_options_cls, patch(
            "app.services.webdriver_service.GeckoDriverManager.install",
            return_value="/path/to/driver",
        ), patch(
            "app.services.webdriver_service.FirefoxService"
        ) as mock_firefox_service_cls, patch(
            "app.services.webdriver_service.webdriver.Firefox"
        ) as mock_firefox_cls:

            options_mock = MagicMock()
            mock_firefox_options_cls.return_value = options_mock
            driver_mock = MagicMock()
            mock_firefox_cls.return_value = driver_mock

            service = WebDriverService()

            mock_load_var.assert_called_once_with("FLASK_ENV", "dev")
            mock_log_info.assert_called_once_with(
                "Configurando o WebDriver...", HTTPStatus.CONTINUE
            )
            options_mock.add_argument.assert_not_called()
            mock_firefox_cls.assert_called_once()
            _, kwargs = mock_firefox_cls.call_args
            self.assertIs(kwargs.get("options"), options_mock)
            self.assertIs(service.driver, driver_mock)

    def test_non_dev_adds_headless_sandbox_flags(self):
        with patch(
            "app.services.webdriver_service.EnvVariablesLoader.load_variable",
            return_value="prod",
        ), patch("app.services.webdriver_service.Logger.log_info"), patch(
            "app.services.webdriver_service.webdriver.FirefoxOptions"
        ) as mock_firefox_options_cls, patch(
            "app.services.webdriver_service.GeckoDriverManager.install",
            return_value="/path/to/driver",
        ), patch(
            "app.services.webdriver_service.FirefoxService"
        ), patch(
            "app.services.webdriver_service.webdriver.Firefox"
        ):

            options_mock = MagicMock()
            mock_firefox_options_cls.return_value = options_mock

            WebDriverService()

            expected_calls = [
                call("--headless"),
                call("--no-sandbox"),
                call("--disable-dev-shm-usage"),
            ]
            self.assertEqual(options_mock.add_argument.call_args_list, expected_calls)

    def test_loads_flask_env_with_default_and_sets_attributes(self):
        with patch(
            "app.services.webdriver_service.EnvVariablesLoader.load_variable",
            return_value="stage",
        ) as mock_load_var, patch(
            "app.services.webdriver_service.Logger.log_info"
        ), patch(
            "app.services.webdriver_service.webdriver.FirefoxOptions"
        ) as mock_firefox_options_cls, patch(
            "app.services.webdriver_service.GeckoDriverManager.install",
            return_value="/path/to/driver",
        ), patch(
            "app.services.webdriver_service.FirefoxService"
        ), patch(
            "app.services.webdriver_service.webdriver.Firefox"
        ):

            options_mock = MagicMock()
            mock_firefox_options_cls.return_value = options_mock

            custom_url = "http://example.com"
            service = WebDriverService(url=custom_url)

            mock_load_var.assert_called_once_with("FLASK_ENV", "dev")
            self.assertEqual(service.flask_env, "stage")
            self.assertEqual(service.url, custom_url)
            self.assertEqual(service.endless_loop_index, -1)

    def test_none_or_empty_env_applies_headless_as_non_dev(self):
        for value in (None, ""):
            with self.subTest(env_value=value), patch(
                "app.services.webdriver_service.EnvVariablesLoader.load_variable",
                return_value=value,
            ), patch("app.services.webdriver_service.Logger.log_info"), patch(
                "app.services.webdriver_service.webdriver.FirefoxOptions"
            ) as mock_firefox_options_cls, patch(
                "app.services.webdriver_service.GeckoDriverManager.install",
                return_value="/path/to/driver",
            ), patch(
                "app.services.webdriver_service.FirefoxService"
            ), patch(
                "app.services.webdriver_service.webdriver.Firefox"
            ):

                options_mock = MagicMock()
                mock_firefox_options_cls.return_value = options_mock

                WebDriverService()

                expected_calls = [
                    call("--headless"),
                    call("--no-sandbox"),
                    call("--disable-dev-shm-usage"),
                ]
                self.assertEqual(
                    options_mock.add_argument.call_args_list, expected_calls
                )

    def test_driver_setup_failure_propagates_and_driver_unset(self):
        with self.subTest("install raises"), patch(
            "app.services.webdriver_service.Logger.log_info"
        ) as mock_log_info, patch(
            "app.services.webdriver_service.webdriver.FirefoxOptions"
        ) as mock_firefox_options_cls, patch(
            "app.services.webdriver_service.GeckoDriverManager.install",
            side_effect=RuntimeError("install fail"),
        ), patch(
            "app.services.webdriver_service.FirefoxService"
        ) as mock_firefox_service_cls, patch(
            "app.services.webdriver_service.webdriver.Firefox"
        ) as mock_firefox_cls:

            options_mock = MagicMock()
            mock_firefox_options_cls.return_value = options_mock

            svc = object.__new__(WebDriverService)
            svc.logger = Logger("WebDriverService")
            svc.flask_env = "dev"

            with self.assertRaises(RuntimeError):
                svc._driver_setup()

            mock_log_info.assert_called_once_with(
                "Configurando o WebDriver...", HTTPStatus.CONTINUE
            )
            mock_firefox_cls.assert_not_called()
            self.assertFalse(hasattr(svc, "driver"))

        with self.subTest("firefox init raises"), patch(
            "app.services.webdriver_service.Logger.log_info"
        ) as mock_log_info, patch(
            "app.services.webdriver_service.webdriver.FirefoxOptions"
        ) as mock_firefox_options_cls, patch(
            "app.services.webdriver_service.GeckoDriverManager.install",
            return_value="/path/to/driver",
        ), patch(
            "app.services.webdriver_service.FirefoxService"
        ) as mock_firefox_service_cls, patch(
            "app.services.webdriver_service.webdriver.Firefox",
            side_effect=RuntimeError("firefox fail"),
        ):

            options_mock = MagicMock()
            mock_firefox_options_cls.return_value = options_mock

            svc = object.__new__(WebDriverService)
            svc.logger = Logger("WebDriverService")
            svc.flask_env = "dev"

            with self.assertRaises(RuntimeError):
                svc._driver_setup()

            mock_log_info.assert_called_once_with(
                "Configurando o WebDriver...", HTTPStatus.CONTINUE
            )
            self.assertFalse(hasattr(svc, "driver"))

    def test_case_sensitive_env_value_results_in_headless(self):
        with patch(
            "app.services.webdriver_service.EnvVariablesLoader.load_variable",
            return_value="DEV",
        ), patch("app.services.webdriver_service.Logger.log_info"), patch(
            "app.services.webdriver_service.webdriver.FirefoxOptions"
        ) as mock_firefox_options_cls, patch(
            "app.services.webdriver_service.GeckoDriverManager.install",
            return_value="/path/to/driver",
        ), patch(
            "app.services.webdriver_service.FirefoxService"
        ), patch(
            "app.services.webdriver_service.webdriver.Firefox"
        ):

            options_mock = MagicMock()
            mock_firefox_options_cls.return_value = options_mock

            WebDriverService()

            expected_calls = [
                call("--headless"),
                call("--no-sandbox"),
                call("--disable-dev-shm-usage"),
            ]
            self.assertEqual(options_mock.add_argument.call_args_list, expected_calls)
