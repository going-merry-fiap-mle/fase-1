import inspect
import json
import logging
import os
from http import HTTPStatus


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        trace_id = getattr(record, "dd.trace_id", None)
        span_id = getattr(record, "dd.span_id", None)
        if trace_id:
            log_record["dd.trace_id"] = str(trace_id)
        if span_id:
            log_record["dd.span_id"] = str(span_id)
        return json.dumps(log_record)


class LogManager:
    @staticmethod
    def setup(level: str | None = None) -> None:
        level_name = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
        try:
            names_map = logging.getLevelNamesMapping()
            log_level = names_map.get(level_name, logging.INFO)
        except Exception:
            log_level = logging.INFO

        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)

        root.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JsonLogFormatter())
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
