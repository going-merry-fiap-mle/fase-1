import os
from http import HTTPStatus
from typing import Any

from dotenv import load_dotenv

from app.utils.logger import Logger


class EnvVariablesLoader:

    def __init__(self, warn_defaults: bool = True) -> None:
        self.logger = Logger("EnvVariablesLoader")
        self.warn_defaults = warn_defaults
        load_dotenv()

    def load_variable(
        self, var_name: str, default_value: Any | None = None
    ) -> Any | None:
        value = os.getenv(var_name, default_value)

        if not value:
            self.__log(var_name, default_value)

        return value

    def __log(self, var_name: str, default_value: Any | None) -> None:
        if self.warn_defaults:
            self.logger.log_warning(
                f"A variável {var_name} não está definida. Valor padrão: {default_value} será usado.",
                HTTPStatus.CONTINUE,
            )
