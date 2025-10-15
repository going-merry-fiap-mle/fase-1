from http import HTTPStatus

from flasgger import Swagger
from flask import Flask

from app.api.register_endpoints import register_endpoints
from app.utils.environment_loader import EnvironmentLoader
from app.utils.logger import AppLogger, LogManager


class FlaskApp:
    def __init__(self) -> None:
        LogManager.setup("INFO")
        self.logger = AppLogger("FlaskApp")

        self.env_loader = EnvironmentLoader()
        self.host: str | None = None
        self.port: int | None = None
        self.debug: bool | None = None

        self._load_variables()

        self.app = Flask(__name__)

        self._configure_swagger()

        register_endpoints(self.app)

    def _load_variables(self) -> None:
        host = self.env_loader.get("HOST", "0.0.0.0")
        port = self.env_loader.get("PORT", 5000)
        debug = self.env_loader.get("DEBUG", False)

        self.host = str(host) if host is not None else "0.0.0.0"

        if isinstance(port, int):
            self.port = port
        elif isinstance(port, str):
            try:
                self.port = int(port)
            except ValueError:
                self.port = 5000
        else:
            self.port = 5000

        self.debug = bool(debug) if debug is not None else False

    def _configure_swagger(self) -> None:
        swagger_template: dict[str, object] = {
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
        self.logger.info("Iniciando a aplicação...", HTTPStatus.CONTINUE)
        self.app.run(debug=self.debug, host=self.host, port=self.port)


flask_app = FlaskApp()

app = flask_app.app

if __name__ == "__main__":
    flask_app.run()
