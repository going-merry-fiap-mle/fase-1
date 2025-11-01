from uuid import UUID

from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.controller.ml.create_prediction_controller import (
    BookNotFoundError,
    CreatePredictionController
)
from app.controller.ml.execute_prediction_controller import ExecutePredictionController
from app.schemas.ml_schema import PredictionBase
from app.services.ml_model_service import BookNotFoundForMLError, MLModelNotLoadedError
from app.utils.logger import AppLogger
from app.utils.request_helpers import parse_boolean_param

ml_bp = Blueprint("ml", __name__, url_prefix="/api/v1/ml")
logger = AppLogger(__name__)


@ml_bp.route("/predictions", methods=["POST"])
def create_prediction() -> Response | tuple[Response, int]:
    r"""
    Criar ou executar predição de Machine Learning
    ---
    tags:
      - ML
    description: |
      Cria uma nova predição ou executa o modelo de ML para gerar uma predição.

      **Comportamento:**
      - Se \`predicted_value\` for fornecido: salva a predição no banco de dados
      - Se \`predicted_value\` não for fornecido: executa o modelo ML para gerar a predição

      **Parâmetros:**
      - book_id (obrigatório): UUID do livro
      - prediction_type (obrigatório): Tipo de predição (ex: "rating_prediction")
      - predicted_value (opcional): Valor predito (se omitido, o modelo será executado)
      - confidence (opcional): Confiança da predição (0.0 a 1.0)
      - model_version (opcional): Versão do modelo usado
      - metadata (opcional): Metadados adicionais em JSON

      **Query Parameters:**
      - use_cache: Se deve usar cache de predições (padrão: true)
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - book_id
            - prediction_type
          properties:
            book_id:
              type: string
              format: uuid
              description: "UUID do livro"
              example: "afdf58a0-ce12-416d-b6fd-9b8ffd097f3c"
            prediction_type:
              type: string
              description: "Tipo de predição"
              example: "rating"
            predicted_value:
              type: string
              description: "Valor predito (opcional - se omitido, o modelo será executado)"
              example: "4.5"
            confidence:
              type: number
              format: float
              minimum: 0.0
              maximum: 1.0
              description: "Confiança da predição"
              example: 0.95
            model_version:
              type: string
              description: "Versão do modelo"
              example: "external_v1.0"
            metadata:
              type: object
              description: "Metadados adicionais"
              example: {"source": "external_api"}
      - name: use_cache
        in: query
        type: boolean
        default: true
        description: "Usar cache de predições (apenas quando predicted_value não for fornecido)"
    responses:
      200:
        description: Predição executada com sucesso (modelo executado)
        schema:
          type: object
          properties:
            prediction:
              type: object
              properties:
                book_id:
                  type: string
                  format: uuid
                book_title:
                  type: string
                predicted_value:
                  type: string
                predicted_label:
                  type: string
                confidence:
                  type: number
                  format: float
                features_used:
                  type: object
                  properties:
                    price:
                      type: number
                    category:
                      type: string
                    availability:
                      type: string
                model_version:
                  type: string
                from_cache:
                  type: boolean
            saved_prediction_id:
              type: string
              format: uuid
      201:
        description: Predição criada com sucesso (valor fornecido)
        schema:
          type: object
          properties:
            prediction:
              type: object
              properties:
                book_id:
                  type: string
                  format: uuid
                book_title:
                  type: string
                predicted_value:
                  type: string
                predicted_label:
                  type: string
                confidence:
                  type: number
                  format: float
                features_used:
                  type: object
                  properties:
                    price:
                      type: number
                    category:
                      type: string
                    availability:
                      type: string
                model_version:
                  type: string
                from_cache:
                  type: boolean
            saved_prediction_id:
              type: string
              format: uuid
      400:
        description: Parâmetros inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid parameters"
            details:
              type: array
              items:
                type: object
            message:
              type: string
      404:
        description: Livro não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Book not found"
            message:
              type: string
      503:
        description: Modelo ML não disponível
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Model not available"
            message:
              type: string
            hint:
              type: string
              example: "Run: python ml_training/train_model.py"
    """
    data = request.get_json()
    prediction_data = PredictionBase(**data)

    logger.info(
        f"ML prediction request - book_id={prediction_data.book_id}, "
        f"type={prediction_data.prediction_type}, "
        f"has_value={prediction_data.predicted_value is not None}"
    )

    if prediction_data.predicted_value is None:
        use_cache = parse_boolean_param(request.args.get('use_cache'), default=True)

        try:
            controller = ExecutePredictionController()
            result = controller.call_controller(
                book_id=UUID(prediction_data.book_id),
                prediction_type=prediction_data.prediction_type,
                use_cache=use_cache
            )

            logger.info(
                f"ML prediction executed - book_id={prediction_data.book_id}, "
                f"from_cache={result.prediction.from_cache}, "
                f"confidence={result.prediction.confidence}"
            )

            return jsonify(result.model_dump())

        except MLModelNotLoadedError as e:
            return jsonify({
                "error": "Model not available",
                "message": str(e),
                "hint": "Run: python ml_training/train_model.py"
            }), 503

        except BookNotFoundForMLError as e:
            return jsonify({
                "error": "Book not found",
                "message": str(e)
            }), 404

    else:
        if prediction_data.confidence is None:
            return jsonify({
                "error": "Bad Request",
                "message": "confidence is required when predicted_value is provided"
            }), 400

        if prediction_data.model_version is None:
            return jsonify({
                "error": "Bad Request",
                "message": "model_version is required when predicted_value is provided"
            }), 400

        try:
            controller = CreatePredictionController()
            result = controller.call_controller(
                book_id=UUID(prediction_data.book_id),
                prediction_type=prediction_data.prediction_type,
                predicted_value=prediction_data.predicted_value,
                confidence=prediction_data.confidence,
                model_version=prediction_data.model_version,
                metadata=prediction_data.metadata
            )

            logger.info(
                f"Prediction saved - id={result.saved_prediction_id}, book_id={prediction_data.book_id}"
            )

            return jsonify(result.model_dump()), 201

        except BookNotFoundError as e:
            return jsonify({
                "error": "Book not found",
                "message": str(e)
            }), 404
