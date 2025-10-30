from typing import Literal
from uuid import UUID

from app.infrastructure.adapters.prediction_adapter import PredictionAdapter
from app.infrastructure.models.book import Book
from app.infrastructure.session_manager import get_session
from app.schemas.ml_schema import MLExecutionResponse, MLPredictionResponse
from app.services.prediction_service import PredictionService
from app.usecases.ml.create_prediction_use_case import CreatePredictionUseCase


class BookNotFoundError(Exception):
    pass


class CreatePredictionController:

    def call_controller(
        self,
        book_id: UUID,
        prediction_type: Literal["rating", "category", "price", "recommendation"],
        predicted_value: str,
        confidence: float,
        model_version: str,
        metadata: dict | None = None
    ) -> MLExecutionResponse:
        book_data = self._get_book_data(book_id)
        if not book_data:
            raise BookNotFoundError(f"Book with id {book_id} not found")

        prediction_adapter = PredictionAdapter()
        prediction_service = PredictionService(prediction_adapter)
        use_case = CreatePredictionUseCase(prediction_service)

        prediction = use_case.execute(
            book_id=book_id,
            prediction_type=prediction_type,
            predicted_value=predicted_value,
            confidence=confidence,
            model_version=model_version,
            metadata=metadata
        )

        features_dict = {
            'price': float(book_data['price']) if book_data['price'] else 0.0,
            'category': book_data['category'],
            'availability': book_data['availability']
        }

        prediction_response = MLPredictionResponse(
            book_id=str(prediction.book_id),
            book_title=book_data['title'],
            predicted_value=prediction.predicted_value,
            predicted_label=prediction.predicted_value,
            confidence=prediction.confidence,
            features_used=features_dict,
            model_version=prediction.model_version,
            from_cache=False
        )

        return MLExecutionResponse(
            prediction=prediction_response,
            saved_prediction_id=str(prediction.id)
        )

    def _get_book_data(self, book_id: UUID) -> dict | None:
        with get_session() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return None
            return {
                'title': book.title,
                'price': book.price,
                'category': book.category.name if book.category else 'Unknown',
                'availability': book.availability
            }
