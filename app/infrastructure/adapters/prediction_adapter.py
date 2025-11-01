from uuid import UUID

from app.domain.models.prediction_domain_model import Prediction
from app.infrastructure.repository.prediction_repository import PredictionRepository
from app.port.prediction_port import IPredictionRepository


class PredictionAdapter(IPredictionRepository):

    def __init__(self) -> None:
        self._repository = PredictionRepository()

    def create_prediction(
        self,
        book_id: UUID,
        prediction_type: str,
        predicted_value: str,
        confidence: float,
        model_version: str,
        metadata: dict | None = None
    ) -> Prediction:
        return self._repository.create_prediction(
            book_id=book_id,
            prediction_type=prediction_type,
            predicted_value=predicted_value,
            confidence=confidence,
            model_version=model_version,
            metadata=metadata
        )
