import os
from http import HTTPStatus

from dotenv import load_dotenv

from app.utils.logger import AppLogger


class EnvironmentLoader:
    def __init__(self, warn_on_default: bool = True) -> None:
        self.logger = AppLogger("EnvLoader")
        self.warn_on_default = warn_on_default
        load_dotenv()

    def get(self, key: str, default: str | int | bool | None = None, required: bool = False) -> str | int | bool | None:

        value = os.getenv(key, default)

        if value is None and (self.warn_on_default or required):
            self.__warn(key, default)

        return value

    def __warn(self, key: str, default: str | int | bool | None) -> None:
        self.logger.warning(
            f"Environment variable '{key}' is not set. Using default value: {default}.",
            HTTPStatus.CONTINUE,
        )
