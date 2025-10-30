from uuid import UUID

from app.domain.models.prediction_domain_model import Prediction
from app.port.prediction_port import IPredictionRepository


class PredictionService:

    def __init__(self, prediction_repository: IPredictionRepository) -> None:
        self._prediction_repository = prediction_repository

    def create_prediction(
        self,
        book_id: UUID,
        prediction_type: str,
        predicted_value: str,
        confidence: float,
        model_version: str,
        metadata: dict | None = None
    ) -> Prediction:
        return self._prediction_repository.create_prediction(
            book_id=book_id,
            prediction_type=prediction_type,
            predicted_value=predicted_value,
            confidence=confidence,
            model_version=model_version,
            metadata=metadata
        )
