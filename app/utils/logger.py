import inspect
import logging
import os
from http import HTTPStatus
from typing import Any, Callable

from pythonjsonlogger import jsonlogger


class ConfigureLogger:

    FORMAT = "%(asctime)s - %(levelname)s - %(message)s %(filename)s"

    def __init__(self, level: int, third_party_level: int) -> None:
        self._configure_loggers(level, third_party_level)
        self._configure_warnings()

    def _configure_loggers(self, level: int, third_party_level: int) -> None:
        root_logger = logging.getLogger()

        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

        root_logger.setLevel(third_party_level)

        handler = logging.StreamHandler()
        handler.setFormatter(jsonlogger.JsonFormatter(self.FORMAT))

        root_logger.addHandler(handler)

        logging.getLogger(__name__).setLevel(level)

        for logger_name in logging.root.manager.loggerDict:
            if logger_name != __name__:
                logging.getLogger(logger_name).setLevel(third_party_level)

    def _configure_warnings(self) -> None:
        logging.captureWarnings(True)
        logger = logging.getLogger("py.warnings")
        logger.setLevel(logging.WARNING)


class Logger:

    def __init__(self, name: str) -> None:
        self._name = name
        self._logger = logging.getLogger(__name__)

    @staticmethod
    def configure(level: str, third_party_level: str) -> None:
        ConfigureLogger(
            logging._nameToLevel[level], logging._nameToLevel[third_party_level]
        )

    @classmethod
    def configure_with_os_variables(cls, level: str, third_party: str) -> str:
        level = os.environ.get(level, logging._levelToName[logging.INFO])
        third_party = os.environ.get(third_party, logging._levelToName[logging.ERROR])

        cls.configure(level, third_party)

    def log_info(self, message: str, status_code: HTTPStatus, **kwargs: Any) -> None:
        self._log(self._logger.info, message, status_code, **kwargs)

    def log_warning(self, message: str, status_code: HTTPStatus, **kwargs: Any) -> None:
        self._log(self._logger.warning, message, status_code, **kwargs)

    def log_error(self, message: str, status_code: HTTPStatus, **kwargs: Any) -> None:
        self._log(self._logger.error, message, status_code, **kwargs)

    def log_exception(
        self, message: str, status_code: HTTPStatus, **kwargs: Any
    ) -> None:
        self._log(self._logger.exception, message, status_code, **kwargs)

    def _log(
        self,
        log_fn: Callable[[dict[str, Any]], None],
        message: str,
        status_code: HTTPStatus,
        **kwargs: Any,
    ) -> None:
        try:
            filename = os.path.basename(
                inspect.currentframe().f_back.f_back.f_code.co_filename
            )
        except Exception:
            filename = "unknown"

        log_fn(
            {
                "message": message,
                "name": self._name,
                "filename": filename,
                "more_information": f"statusCode: {status_code}",
                **kwargs,
            }
        )
