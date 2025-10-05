import inspect
import logging
import os
from http import HTTPStatus
from typing import Optional


class LogFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        try:
            frame = inspect.currentframe()
            outer_frames = inspect.getouterframes(frame)
            caller = next((f for f in outer_frames if f.filename != __file__), None)
            filename = os.path.basename(caller.filename) if caller else "unknown"
        except Exception:
            filename = "unknown"

        base_format = (
            f"[%(asctime)s] [%(levelname)s] "
            f"%(message)s | logger=%(name)s | file={filename}"
        )

        formatter = logging.Formatter(base_format, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class LogManager:
    @staticmethod
    def setup(level: Optional[str] = None) -> None:
        level_name = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
        log_level = logging._nameToLevel.get(level_name, logging.INFO)

        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)

        root.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(LogFormatter())
        root.addHandler(console_handler)

        logging.captureWarnings(True)


class AppLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def _log(self, level: str, message: str, status: HTTPStatus) -> None:
        try:
            caller_file = os.path.basename(inspect.stack()[2].filename)
        except Exception:
            caller_file = "unknown"

        log_data: dict[str, int | str] = {
            "message": message,
            "status_code": status.value,
            "file": caller_file,
        }

        getattr(self.logger, level)(str(log_data))

    def info(self, message: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        self._log("info", message, status)

    def warning(
        self, message: str, status: HTTPStatus = HTTPStatus.BAD_REQUEST
    ) -> None:
        self._log("warning", message, status)

    def error(
        self, message: str, status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> None:
        self._log("error", message, status)

    def exception(
        self, message: str, status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> None:
        self._log("exception", message, status)
