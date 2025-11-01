import uuid
from typing import Self

from sqlalchemy import (
    CheckConstraint,
    Column,
    Float,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.domain.models.prediction_domain_model import Prediction as PredictionDomain

from .base import Base, TimestampMixin


class Prediction(TimestampMixin, Base):
    __tablename__ = "predictions"
    __table_args__ = (
        CheckConstraint(
            "(confidence >= 0.0 AND confidence <= 1.0)", name="check_confidence_range"
        ),
        UniqueConstraint("id", name="uq_predictions_id"),
        Index("ix_predictions_book_id", "book_id"),
        Index("ix_predictions_prediction_type", "prediction_type"),
        Index("ix_predictions_created_at", "created_at"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    book_id = Column(
        UUID(as_uuid=True), ForeignKey("books.id"), nullable=False
    )
    prediction_type = Column(String, nullable=False)
    predicted_value = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(String, nullable=False)
    prediction_metadata = Column(JSON, nullable=True)

    book = relationship("Book", backref="predictions")

    @classmethod
    def from_domain(cls, prediction: PredictionDomain) -> Self:
        return cls(
            id=prediction.id,  # type: ignore
            book_id=prediction.book_id,  # type: ignore
            prediction_type=prediction.prediction_type,  # type: ignore
            predicted_value=prediction.predicted_value,  # type: ignore
            confidence=prediction.confidence,  # type: ignore
            model_version=prediction.model_version,  # type: ignore
            prediction_metadata=prediction.metadata,  # type: ignore
        )

    def to_domain(self) -> PredictionDomain:
        return PredictionDomain(
            id=self.id,  # type: ignore
            book_id=self.book_id,  # type: ignore
            prediction_type=self.prediction_type,  # type: ignore
            predicted_value=self.predicted_value,  # type: ignore
            confidence=self.confidence,  # type: ignore
            model_version=self.model_version,  # type: ignore
            metadata=self.prediction_metadata,  # type: ignore
            created_at=self.created_at,  # type: ignore
        )
