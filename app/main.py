from http import HTTPStatus
from typing import Any

from flasgger import Swagger
from flask import Flask

from app.api.register_endpoints import register_endpoints
from app.utils.environment_loader import EnvironmentLoader
from app.utils.logger import AppLogger, LogManager

from infrastructure.database import engine, SessionLocal
from sqlalchemy.exc import OperationalError


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

        self._db_connection()

        register_endpoints(self.app)

    def _load_variables(self) -> None:
        self.host = self.env_loader.get("HOST", "0.0.0.0")
        self.port = self.env_loader.get("PORT", 5000)
        self.debug = self.env_loader.get("DEBUG", False)

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
        self.logger.info("Iniciando a aplicação...", HTTPStatus.CONTINUE)
        self.app.run(debug=self.debug, host=self.host, port=self.port)

    def _db_connection(self) -> None:
        try:
            with engine.connect() as conn:
                self.logger.info("Banco de dados conectado com sucesso.")
                pass
        except OperationalError as e:
            self.logger.error("Falha na conexão com o banco de dados:", e)


flask_app = FlaskApp()

app = flask_app.app

if __name__ == "__main__":
    flask_app.run()
