from http import HTTPStatus

from flasgger import Swagger
from flask import Flask, jsonify
from pydantic import ValidationError

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
        self._register_error_handlers()


        register_endpoints(self.app)

    def _load_variables(self) -> None:
        self.host = str(self.env_loader.get("HOST", "0.0.0.0") or "0.0.0.0")
        self.port = int(self.env_loader.get("PORT", 5000) or 5000)
        self.debug = bool(self.env_loader.get("DEBUG", False))

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

    def _register_error_handlers(self) -> None:
        @self.app.errorhandler(ValidationError)
        def handle_validation_error(error: ValidationError):
            self.logger.warning(f"Validation error: {error.errors()}")
            return jsonify({"error": "Invalid parameters", "details": error.errors()}), 400

        @self.app.errorhandler(ValueError)
        def handle_value_error(error: ValueError):
            self.logger.warning(f"Value error: {str(error)}")
            return jsonify({"error": "Invalid value", "message": str(error)}), 400

        @self.app.errorhandler(Exception)
        def handle_generic_error(error: Exception):
            self.logger.exception(f"Unhandled exception: {str(error)}")
            return jsonify({"error": "Internal server error", "message": str(error)}), 500

    def run(self) -> None:
        self.logger.info("Iniciando a aplicação...", HTTPStatus.CONTINUE)
        self.app.run(debug=self.debug, host=self.host, port=self.port)

flask_app = FlaskApp()

app = flask_app.app

if __name__ == "__main__":
    flask_app.run()
