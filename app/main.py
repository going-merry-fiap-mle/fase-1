from http import HTTPStatus
from pathlib import Path
import subprocess

from flasgger import Swagger
from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from app.api.register_endpoints import register_endpoints
from app.ml.model_loader import ml_loader
from app.services.ml_model_service import BookNotFoundForMLError, MLModelNotLoadedError
from app.utils.environment_loader import EnvironmentLoader
from app.utils.logger import AppLogger, LogManager
from app.api.auth import router as auth_router



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
        self._load_ml_models()

        register_endpoints(self.app)
        self.app.register_blueprint(auth_router)

    def _load_variables(self) -> None:
        self.host = str(self.env_loader.get("HOST", "0.0.0.0") or "0.0.0.0")
        self.port = int(self.env_loader.get("PORT", 5000) or 5000)
        self.debug = bool(self.env_loader.get("DEBUG", False))

    def _load_ml_models(self) -> None:
        """Carregar modelos de Machine Learning na inicialização"""
        self._ensure_ml_model()
        try:
            # ml_loader já é carregado no import do topo do arquivo
            self.logger.info("Modelos ML carregados com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao carregar modelos ML: {str(e)}")

    def _ensure_ml_model(self) -> None:
        """Garante que modelo ML existe, treina automaticamente se necessário"""
        model_path = Path("models/rating_classifier_v1.pkl")

        if model_path.exists():
            self.logger.info("ML model found, ready to serve predictions")
            return

        self.logger.info("ML model not found, initiating automatic training...")

        try:
            result = subprocess.run(
                ["python", "ml_training/train_model.py"],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=Path(__file__).parent.parent
            )

            if result.returncode == 0:
                self.logger.info("ML model trained successfully")
                if result.stdout:
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            self.logger.info(f"[Training] {line}")
            else:
                self.logger.warning(f"ML training failed with code {result.returncode}")
                if result.stderr:
                    self.logger.warning(f"Training error: {result.stderr}")
        except subprocess.TimeoutExpired:
            self.logger.error("ML training timeout (exceeded 5 minutes)")
        except FileNotFoundError:
            self.logger.error("Training script not found: ml_training/train_model.py")
        except Exception as e:
            self.logger.error(f"ML training error: {str(e)}")

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
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
                }
            },
            "security": [
                {"Bearer": []}
            ]
        }
        Swagger(self.app, template=swagger_template)

    def _register_error_handlers(self) -> None:
        @self.app.errorhandler(ValidationError)
        def handle_validation_error(error: ValidationError):
            self.logger.warning(f"Validation error: {error.errors()}")
            errors = []
            for err in error.errors():
                serializable_err = {
                    "field": ".".join(str(x) for x in err.get("loc", [])),
                    "message": err.get("msg", ""),
                    "type": err.get("type", "")
                }
                errors.append(serializable_err)
            return jsonify({"error": "Invalid parameters", "details": errors}), HTTPStatus.BAD_REQUEST

        @self.app.errorhandler(UnsupportedMediaType)
        def handle_unsupported_media_type(error: UnsupportedMediaType):
            self.logger.warning(f"Unsupported media type: {str(error)}")
            return jsonify({
                "error": "Invalid parameters",
                "message": "Content-Type must be application/json"
            }), HTTPStatus.BAD_REQUEST

        @self.app.errorhandler(ValueError)
        def handle_value_error(error: ValueError):
            self.logger.warning(f"Value error: {str(error)}")
            error_msg = str(error)
            if "not found" in error_msg.lower():
                error_type = "Book not found" if "book" in error_msg.lower() else "Not found"
                return jsonify({"error": error_type, "message": error_msg}), HTTPStatus.NOT_FOUND
            if "uuid" in error_msg.lower() or "hexadecimal" in error_msg.lower():
                return jsonify({"error": "Invalid parameters", "message": error_msg}), HTTPStatus.BAD_REQUEST
            return jsonify({"error": "Invalid value", "message": error_msg}), HTTPStatus.BAD_REQUEST

        @self.app.errorhandler(MLModelNotLoadedError)
        def handle_ml_model_not_loaded_error(error: MLModelNotLoadedError):
            self.logger.warning(f"ML Model not loaded: {str(error)}")
            return jsonify({
                "error": "Model not available",
                "message": str(error),
                "hint": "Model should train automatically on startup. Check application logs for training errors."
            }), HTTPStatus.SERVICE_UNAVAILABLE

        @self.app.errorhandler(BookNotFoundForMLError)
        def handle_book_not_found_for_ml_error(error: BookNotFoundForMLError):
            self.logger.warning(f"Book not found for ML: {str(error)}")
            return jsonify({"error": "Book not found", "message": str(error)}), HTTPStatus.NOT_FOUND

        @self.app.errorhandler(Exception)
        def handle_generic_error(error: Exception):
            self.logger.exception(f"Unhandled exception: {str(error)}")
            return jsonify({"error": "Internal server error", "message": str(error)}), HTTPStatus.INTERNAL_SERVER_ERROR

    def run(self) -> None:
        self.logger.info("Iniciando a aplicação...", HTTPStatus.CONTINUE)
        self.app.run(debug=self.debug, host=self.host, port=self.port)

flask_app = FlaskApp()

app = flask_app.app

if __name__ == "__main__":
    flask_app.run()
