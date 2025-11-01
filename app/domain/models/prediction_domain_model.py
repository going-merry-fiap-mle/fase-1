from datetime import datetime
from typing import Literal
from uuid import UUID


class Prediction:

    def __init__(
        self,
        id: UUID,
        book_id: UUID,
        prediction_type: Literal["rating", "category", "price", "recommendation"],
        predicted_value: str,
        confidence: float,
        model_version: str,
        metadata: dict | None,
        created_at: datetime,
    ) -> None:
        self.id = id
        self.book_id = book_id
        self.prediction_type = prediction_type
        self.predicted_value = predicted_value
        self.confidence = confidence
        self.model_version = model_version
        self.metadata = metadata
        self.created_at = created_at
