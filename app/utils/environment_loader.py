import os
from http import HTTPStatus
from typing import Any

from dotenv import load_dotenv

from app.utils.logger import AppLogger


class EnvironmentLoader:
    def __init__(self, warn_on_default: bool = True) -> None:
        self.logger = AppLogger("EnvLoader")
        self.warn_on_default = warn_on_default
        load_dotenv()

    def get(self, key: str, default: Any = None, required: bool = False) -> Any:

        value = os.getenv(key, default)

        if value is None and (self.warn_on_default or required):
            self.__warn(key, default)

        return value

    def __warn(self, key: str, default: Any) -> None:
        self.logger.warning(
            f"Environment variable '{key}' is not set. Using default value: {default}.",
            HTTPStatus.CONTINUE,
        )
