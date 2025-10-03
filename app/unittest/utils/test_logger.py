import logging
import os
import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from app.utils.logger import Logger


class TestLogger(unittest.TestCase):
    def test_log_info_includes_context_and_status_code(self):
        with patch("app.utils.logger.logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            logger = Logger("my-service")
            logger.log_info("hello", HTTPStatus.OK)

            mock_logger.info.assert_called_once()
            args, _ = mock_logger.info.call_args
            payload = args[0]

            self.assertIsInstance(payload, dict)
            self.assertEqual(payload["message"], "hello")
            self.assertEqual(payload["name"], "my-service")
            self.assertEqual(payload["filename"], os.path.basename(__file__))
            self.assertEqual(
                payload["more_information"], f"statusCode: {HTTPStatus.OK}"
            )

    def test_log_warning_includes_context_and_status_code(self):
        with patch("app.utils.logger.logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            logger = Logger("my-service")
            logger.log_warning("hello", HTTPStatus.OK)

            mock_logger.warning.assert_called_once()
            args, _ = mock_logger.warning.call_args
            payload = args[0]

            self.assertIsInstance(payload, dict)
            self.assertEqual(payload["message"], "hello")
            self.assertEqual(payload["name"], "my-service")
            self.assertEqual(payload["filename"], os.path.basename(__file__))
            self.assertEqual(
                payload["more_information"], f"statusCode: {HTTPStatus.OK}"
            )

    def test_log_error_includes_context_and_status_code(self):
        with patch("app.utils.logger.logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            logger = Logger("my-service")
            logger.log_error("hello", HTTPStatus.OK)

            mock_logger.error.assert_called_once()
            args, _ = mock_logger.error.call_args
            payload = args[0]

            self.assertIsInstance(payload, dict)
            self.assertEqual(payload["message"], "hello")
            self.assertEqual(payload["name"], "my-service")
            self.assertEqual(payload["filename"], os.path.basename(__file__))
            self.assertEqual(
                payload["more_information"], f"statusCode: {HTTPStatus.OK}"
            )

    def test_log_exception_calls_exception_method(self):
        with patch("app.utils.logger.logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            logger = Logger("svc")
            try:
                raise ValueError("boom")
            except Exception:
                logger.log_exception("error occurred", HTTPStatus.INTERNAL_SERVER_ERROR)

            mock_logger.exception.assert_called_once()
            args, _ = mock_logger.exception.call_args
            payload = args[0]
            self.assertEqual(payload["message"], "error occurred")
            self.assertEqual(payload["name"], "svc")
            self.assertEqual(
                payload["more_information"],
                f"statusCode: {HTTPStatus.INTERNAL_SERVER_ERROR}",
            )

    def test_configure_maps_level_names_to_ints(self):
        with patch("app.utils.logger.ConfigureLogger") as mock_configure_logger:
            Logger.configure("INFO", "WARNING")
            mock_configure_logger.assert_called_once_with(logging.INFO, logging.WARNING)

    def test_configure_with_env_uses_defaults_when_missing(self):
        with patch.object(Logger, "configure") as mock_configure, patch(
            "app.utils.logger.os.environ", new={}
        ):
            Logger.configure_with_os_variables("APP_LOG_LEVEL", "THIRD_PARTY_LOG_LEVEL")
            mock_configure.assert_called_once_with("INFO", "ERROR")

    def test_log_sets_filename_unknown_on_inspect_failure(self):
        with patch("app.utils.logger.logging.getLogger") as mock_get_logger, patch(
            "app.utils.logger.inspect.currentframe", side_effect=Exception("fail")
        ):
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            logger = Logger("svc")
            logger.log_info("msg", HTTPStatus.CREATED)

            mock_logger.info.assert_called_once()
            payload = mock_logger.info.call_args[0][0]
            self.assertEqual(payload["filename"], "unknown")
            self.assertEqual(payload["message"], "msg")
