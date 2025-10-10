import unittest
from http import HTTPStatus
from unittest.mock import patch

from app.utils.environment_loader import EnvironmentLoader


class TestEnvironmentLoader(unittest.TestCase):
    def test_returns_existing_env_value_without_warning(self):
        with patch(
            "app.utils.environment_loader.load_dotenv"
        ) as load_dotenv_mock, patch(
            "app.utils.environment_loader.AppLogger"
        ) as AppLoggerMock, patch(
            "app.utils.environment_loader.os.getenv"
        ) as getenv_mock:
            getenv_mock.return_value = "present_value"

            loader = EnvironmentLoader()
            value = loader.get("EXISTING_KEY")

            self.assertEqual(value, "present_value")
            AppLoggerMock.return_value.warning.assert_not_called()

    def test_loads_dotenv_on_initialization_allows_env_from_file(self):
        with patch(
            "app.utils.environment_loader.load_dotenv"
        ) as load_dotenv_mock, patch(
            "app.utils.environment_loader.AppLogger"
        ) as AppLoggerMock, patch(
            "app.utils.environment_loader.os.getenv"
        ) as getenv_mock:
            getenv_mock.return_value = "value_from_env"

            loader = EnvironmentLoader()
            load_dotenv_mock.assert_called_once()

            value = loader.get("KEY_FROM_ENV_FILE")
            self.assertEqual(value, "value_from_env")
            AppLoggerMock.return_value.warning.assert_not_called()

    def test_returns_default_when_missing_without_warning(self):
        with patch("app.utils.environment_loader.load_dotenv"), patch(
            "app.utils.environment_loader.AppLogger"
        ) as AppLoggerMock, patch(
            "app.utils.environment_loader.os.getenv"
        ) as getenv_mock:
            getenv_mock.side_effect = lambda key, default=None: default

            loader = EnvironmentLoader()
            value = loader.get("MISSING_KEY", default="fallback")

            self.assertEqual(value, "fallback")
            AppLoggerMock.return_value.warning.assert_not_called()

    def test_warns_when_missing_and_no_default_with_warn_on_default(self):
        with patch("app.utils.environment_loader.load_dotenv"), patch(
            "app.utils.environment_loader.AppLogger"
        ) as AppLoggerMock, patch(
            "app.utils.environment_loader.os.getenv"
        ) as getenv_mock:
            getenv_mock.return_value = None

            loader = EnvironmentLoader(warn_on_default=True)
            value = loader.get("UNSET_KEY")

            self.assertIsNone(value)
            expected_message = "Environment variable 'UNSET_KEY' is not set. Using default value: None."
            AppLoggerMock.return_value.warning.assert_called_once_with(
                expected_message, HTTPStatus.CONTINUE
            )

    def test_warns_when_missing_and_required_even_if_warn_disabled(self):
        with patch("app.utils.environment_loader.load_dotenv"), patch(
            "app.utils.environment_loader.AppLogger"
        ) as AppLoggerMock, patch(
            "app.utils.environment_loader.os.getenv"
        ) as getenv_mock:
            getenv_mock.return_value = None

            loader = EnvironmentLoader(warn_on_default=False)
            value = loader.get("REQUIRED_KEY", required=True)

            self.assertIsNone(value)
            expected_message = "Environment variable 'REQUIRED_KEY' is not set. Using default value: None."
            AppLoggerMock.return_value.warning.assert_called_once_with(
                expected_message, HTTPStatus.CONTINUE
            )

    def test_required_true_with_non_none_default_returns_default_without_warning(self):
        with patch("app.utils.environment_loader.load_dotenv"), patch(
            "app.utils.environment_loader.AppLogger"
        ) as AppLoggerMock, patch(
            "app.utils.environment_loader.os.getenv"
        ) as getenv_mock:
            getenv_mock.side_effect = lambda key, default=None: default

            loader = EnvironmentLoader(warn_on_default=False)
            value = loader.get(
                "MISSING_BUT_REQUIRED", default="provided_default", required=True
            )

            self.assertEqual(value, "provided_default")
            AppLoggerMock.return_value.warning.assert_not_called()
