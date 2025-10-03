import unittest
from http import HTTPStatus
from unittest.mock import patch

from app.utils.env_variables_loader import EnvVariablesLoader


class TestEnvVariablesLoader(unittest.TestCase):

    @patch("app.utils.env_variables_loader.load_dotenv")
    @patch("app.utils.env_variables_loader.Logger")
    @patch("app.utils.env_variables_loader.os.getenv", return_value="present_value")
    def test_returns_env_value_without_warning(
        self, mock_getenv, mock_logger_cls, mock_load_dotenv
    ):
        loader = EnvVariablesLoader()
        result = loader.load_variable("EXISTING_VAR", default_value="default_value")

        self.assertEqual(result, "present_value")
        mock_logger = mock_logger_cls.return_value
        mock_logger.log_warn.assert_not_called()

    @patch("app.utils.env_variables_loader.load_dotenv")
    @patch("app.utils.env_variables_loader.Logger")
    def test_loads_dotenv_on_init(self, mock_logger_cls, mock_load_dotenv):
        EnvVariablesLoader()
        mock_load_dotenv.assert_called_once_with()

    @patch("app.utils.env_variables_loader.load_dotenv")
    @patch("app.utils.env_variables_loader.Logger")
    @patch("app.utils.env_variables_loader.os.getenv", return_value="env_precedence")
    def test_env_value_takes_precedence_over_default(
        self, mock_getenv, mock_logger_cls, mock_load_dotenv
    ):
        loader = EnvVariablesLoader()
        result = loader.load_variable("VAR_WITH_DEFAULT", default_value="fallback")

        self.assertEqual(result, "env_precedence")
        mock_logger = mock_logger_cls.return_value
        mock_logger.log_warn.assert_not_called()

    @patch("app.utils.env_variables_loader.load_dotenv")
    @patch("app.utils.env_variables_loader.Logger")
    @patch("app.utils.env_variables_loader.os.getenv", return_value=None)
    def test_missing_var_returns_default_and_logs_warning(
        self, mock_getenv, mock_logger_cls, mock_load_dotenv
    ):
        loader = EnvVariablesLoader()
        var_name = "MISSING_VAR"
        default_value = None

        result = loader.load_variable(var_name, default_value=default_value)

        self.assertIsNone(result)
        mock_logger = mock_logger_cls.return_value
        mock_logger.log_warning.assert_called_once()
        args, kwargs = mock_logger.log_warning.call_args
        self.assertEqual(args[1], HTTPStatus.CONTINUE)
        self.assertIn(var_name, args[0])
        self.assertIn("Valor padrão", args[0])

    @patch("app.utils.env_variables_loader.load_dotenv")
    @patch("app.utils.env_variables_loader.Logger")
    @patch("app.utils.env_variables_loader.os.getenv", return_value=None)
    def test_no_warning_when_warn_defaults_is_false(
        self, mock_getenv, mock_logger_cls, mock_load_dotenv
    ):
        loader = EnvVariablesLoader(warn_defaults=False)
        result = loader.load_variable("MISSING_VAR", default_value=None)

        self.assertIsNone(result)
        mock_logger = mock_logger_cls.return_value
        mock_logger.log_warn.assert_not_called()

    @patch("app.utils.env_variables_loader.load_dotenv")
    @patch("app.utils.env_variables_loader.Logger")
    @patch("app.utils.env_variables_loader.os.getenv", return_value="")
    def test_empty_string_value_logs_warning_but_is_returned(
        self, mock_getenv, mock_logger_cls, mock_load_dotenv
    ):
        loader = EnvVariablesLoader()
        result = loader.load_variable("EMPTY_STRING_VAR", default_value="fallback")

        self.assertEqual(result, "")
        mock_logger = mock_logger_cls.return_value
        mock_logger.log_warning.assert_called_once()
        args, kwargs = mock_logger.log_warning.call_args
        self.assertEqual(args[1], HTTPStatus.CONTINUE)
