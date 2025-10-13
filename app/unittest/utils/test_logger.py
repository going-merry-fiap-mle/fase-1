import logging
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import app.utils.logger as logger_module
from app.utils.logger import AppLogger, LogFormatter, LogManager


class TestLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.root_logger = logging.getLogger()
        self.original_handlers = self.root_logger.handlers[:]
        self.original_level = self.root_logger.level

    def tearDown(self) -> None:
        for handler in self.root_logger.handlers[:]:
            self.root_logger.removeHandler(handler)
        for handler in self.original_handlers:
            self.root_logger.addHandler(handler)
        self.root_logger.setLevel(self.original_level)

    def test_setup_sets_root_level_and_installs_logformatter(self) -> None:
        LogManager.setup(level="DEBUG")

        handlers = self.root_logger.handlers
        self.assertEqual(len(handlers), 1)
        handler = handlers[0]
        self.assertIsInstance(handler, logging.StreamHandler)
        self.assertIsNotNone(handler.formatter)
        self.assertIsInstance(handler.formatter, LogFormatter)
        self.assertEqual(self.root_logger.level, logging.DEBUG)

    def test_logging_methods_emit_expected_levels_and_default_statuses(self) -> None:
        mock_logger = MagicMock()
        with patch("logging.getLogger", return_value=mock_logger):
            app_logger = AppLogger("test-logger")
            app_logger.info("info-message")
            app_logger.warning("warn-message")
            app_logger.error("error-message")
            app_logger.exception("exception-message")

        mock_logger.info.assert_called_once()
        mock_logger.warning.assert_called_once()
        mock_logger.error.assert_called_once()
        mock_logger.exception.assert_called_once()

        info_arg = mock_logger.info.call_args[0][0]
        warn_arg = mock_logger.warning.call_args[0][0]
        error_arg = mock_logger.error.call_args[0][0]
        exception_arg = mock_logger.exception.call_args[0][0]

        self.assertIn("status_code", info_arg)
        self.assertIn("200", info_arg)
        self.assertIn("status_code", warn_arg)
        self.assertIn("400", warn_arg)
        self.assertIn("status_code", error_arg)
        self.assertIn("500", error_arg)
        self.assertIn("status_code", exception_arg)
        self.assertIn("500", exception_arg)

    def test_formatter_includes_caller_filename_and_logger_name(self) -> None:
        fake_frames = [
            SimpleNamespace(filename=logger_module.__file__),
            SimpleNamespace(filename="/some/path/caller_module.py"),
        ]

        with patch("inspect.currentframe") as mock_currentframe, patch(
            "inspect.getouterframes", return_value=fake_frames
        ):
            mock_currentframe.return_value = object()
            formatter = LogFormatter()
            record = logging.LogRecord(
                name="mylogger",
                level=logging.INFO,
                pathname="/path/to/something.py",
                lineno=42,
                msg="hello world",
                args=(),
                exc_info=None,
            )
            formatted = formatter.format(record)

        self.assertIn("logger=mylogger", formatted)
        self.assertIn("hello world", formatted)

    def test_setup_falls_back_to_info_on_invalid_level(self):
        LogManager.setup(level="NOT_A_LEVEL")

        self.assertEqual(self.root_logger.level, logging.INFO)

        self.assertTrue(self.root_logger.handlers)
        self.assertIsInstance(self.root_logger.handlers[0].formatter, LogFormatter)

    def test_formatter_uses_unknown_file_on_inspect_failure(self):
        with patch("inspect.currentframe", side_effect=RuntimeError("boom")):
            formatter = LogFormatter()
            record = logging.LogRecord(
                name="mylogger",
                level=logging.INFO,
                pathname="/path/to/something.py",
                lineno=100,
                msg="message",
                args=(),
                exc_info=None,
            )
            formatted = formatter.format(record)

        self.assertIsInstance(formatted, str)
        self.assertIn("logger=mylogger", formatted)

    def test_app_logger_uses_unknown_file_on_stack_failure(self):
        mock_logger = MagicMock()
        with patch("logging.getLogger", return_value=mock_logger), patch(
            "inspect.stack", side_effect=RuntimeError("stack fail")
        ):
            app_logger = AppLogger("logger-name")
            app_logger.info("payload")

        mock_logger.info.assert_called_once()
        arg = mock_logger.info.call_args[0][0]
        self.assertIn("'file': 'unknown'", arg)
