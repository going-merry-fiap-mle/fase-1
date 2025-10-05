import unittest
from unittest.mock import MagicMock, call, patch

from app.infrastructure.webdriver_infrastructure import WebDriverInfrastructure


class TestWebDriverInfrastructure(unittest.TestCase):
    def setUp(self):
        self.patcher_logger = patch(
            "app.infrastructure.webdriver_infrastructure.AppLogger"
        )
        self.patcher_env_loader = patch(
            "app.infrastructure.webdriver_infrastructure.EnvironmentLoader"
        )
        self.patcher_firefox = patch(
            "app.infrastructure.webdriver_infrastructure.webdriver.Firefox"
        )
        self.patcher_firefox_options = patch(
            "app.infrastructure.webdriver_infrastructure.webdriver.FirefoxOptions"
        )
        self.patcher_gdm = patch(
            "app.infrastructure.webdriver_infrastructure.GeckoDriverManager"
        )
        self.patcher_service = patch(
            "app.infrastructure.webdriver_infrastructure.FirefoxService"
        )

        self.mock_logger_class = self.patcher_logger.start()
        self.mock_env_loader_class = self.patcher_env_loader.start()
        self.mock_driver_class = self.patcher_firefox.start()
        self.mock_options_class = self.patcher_firefox_options.start()
        self.mock_gdm_class = self.patcher_gdm.start()
        self.mock_service_class = self.patcher_service.start()

        self.env_loader_instance = self.mock_env_loader_class.return_value
        self.options_instance = MagicMock()
        self.mock_options_class.return_value = self.options_instance

    def tearDown(self):
        self.patcher_service.stop()
        self.patcher_gdm.stop()
        self.patcher_firefox_options.stop()
        self.patcher_firefox.stop()
        self.patcher_env_loader.stop()
        self.patcher_logger.stop()

    def test_initializes_headless_when_not_dev_env(self):
        self.env_loader_instance.get.return_value = "prod"
        self.mock_gdm_class.return_value.install.return_value = "/path/to/geckodriver"

        svc = WebDriverInfrastructure()

        self.options_instance.add_argument.assert_has_calls(
            [
                call("--headless"),
                call("--no-sandbox"),
                call("--disable-dev-shm-usage"),
            ],
            any_order=False,
        )
        self.assertEqual(self.options_instance.add_argument.call_count, 3)

        args, kwargs = self.mock_driver_class.call_args
        self.assertIs(kwargs["options"], self.options_instance)
        self.mock_service_class.assert_called_once_with("/path/to/geckodriver")
        self.assertIs(kwargs["service"], self.mock_service_class.return_value)
        self.assertEqual(svc.flask_env, "prod")

    def test_defaults_to_dev_env_without_headless(self):
        self.env_loader_instance.get.side_effect = lambda key, default: default
        self.mock_gdm_class.return_value.install.return_value = "/path/to/geckodriver"

        svc = WebDriverInfrastructure()

        self.env_loader_instance.get.assert_called_once_with("FLASK_ENV", "dev")
        self.assertEqual(svc.flask_env, "dev")
        self.options_instance.add_argument.assert_not_called()

    def test_uses_provided_url_on_init(self):
        self.env_loader_instance.get.side_effect = lambda key, default: default
        self.mock_gdm_class.return_value.install.return_value = "/path/to/geckodriver"

        custom_url = "https://example.com/"
        svc = WebDriverInfrastructure(custom_url)

        self.assertEqual(svc.url, custom_url)

    def test_case_sensitive_flask_env_triggers_headless(self):
        self.env_loader_instance.get.return_value = "DEV"
        self.mock_gdm_class.return_value.install.return_value = "/path/to/geckodriver"

        WebDriverInfrastructure()

        self.options_instance.add_argument.assert_has_calls(
            [
                call("--headless"),
                call("--no-sandbox"),
                call("--disable-dev-shm-usage"),
            ],
            any_order=False,
        )
        self.assertEqual(self.options_instance.add_argument.call_count, 3)

    def test_geckodriver_install_failure_is_propagated(self):
        self.env_loader_instance.get.return_value = "prod"
        self.mock_gdm_class.return_value.install.side_effect = Exception(
            "install failed"
        )

        with self.assertRaises(Exception) as ctx:
            WebDriverInfrastructure()

        self.assertIn("install failed", str(ctx.exception))
        self.mock_driver_class.assert_not_called()

    def test_webdriver_initialization_failure_is_propagated(self):
        self.env_loader_instance.get.return_value = "prod"
        self.mock_gdm_class.return_value.install.return_value = "/path/to/geckodriver"
        self.mock_driver_class.side_effect = Exception("webdriver init failed")

        with self.assertRaises(Exception) as ctx:
            WebDriverInfrastructure()

        self.assertIn("webdriver init failed", str(ctx.exception))
        self.mock_service_class.assert_called_once_with("/path/to/geckodriver")
