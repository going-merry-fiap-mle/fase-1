from http import HTTPStatus
from typing import Any

from flasgger import Swagger
from flask import Flask

from app.api.register_endpoints import register_endpoints
from app.utils.env_variables_loader import EnvVariablesLoader
from app.utils.logger import Logger


class FlaskApp:
    def __init__(self) -> None:
        self.logger = Logger("FlaskApp")
        self.logger.configure_with_os_variables("LOG_LEVEL", "THIRD_PARTY_LOG_LEVEL")

        self.env_loader = EnvVariablesLoader()
        self.host: str | None = None
        self.port: int | None = None
        self.debug: bool | None = None

        self._load_variables()

        self.app = Flask(__name__)

        self._configure_swagger()

        register_endpoints(self.app)

    def _load_variables(self) -> None:
        self.host = self.env_loader.load_variable("HOST", "0.0.0.0")
        self.port = self.env_loader.load_variable("PORT", 5000)
        self.debug = self.env_loader.load_variable("DEBUG", False)

    def _configure_swagger(self) -> None:
        swagger_template: dict[str, Any] = {
            "swagger": "2.0",
            "info": {
                "title": "API Livros FIAP",
                "description": "Projeto da Fase 1 da Pós em Machine Learning Engineering - Equipe Going Merry",
                "version": "1.0.0",
                "license": {"name": "MIT"},
            },
            "basePath": "/",
            "schemes": ["http", "https"],
        }
        Swagger(self.app, template=swagger_template)

    def run(self) -> None:
        self.logger.log_info("Iniciando a aplicação...", HTTPStatus.CONTINUE)
        self.app.run(debug=self.debug, host=self.host, port=self.port)


flask_app = FlaskApp()

if __name__ == "__main__":
    flask_app.run()
