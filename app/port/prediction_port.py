from typing import Protocol
from uuid import UUID

from app.domain.models.prediction_domain_model import Prediction


class IPredictionRepository(Protocol):

    def create_prediction(
        self,
        book_id: UUID,
        prediction_type: str,
        predicted_value: str,
        confidence: float,
        model_version: str,
        metadata: dict | None = None
    ) -> Prediction: ...
