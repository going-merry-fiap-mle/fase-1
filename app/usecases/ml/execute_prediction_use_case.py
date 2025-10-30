from uuid import UUID

from app.ml.constants import DEFAULT_MODEL_VERSION
from app.services.ml_model_service import MLModelService
from app.services.prediction_service import PredictionService


class ExecutePredictionUseCase:

    def __init__(
        self,
        ml_model_service: MLModelService,
        prediction_service: PredictionService
    ) -> None:
        self._ml_model_service = ml_model_service
        self._prediction_service = prediction_service

    def execute(
        self,
        book_id: UUID,
        prediction_type: str,
        use_cache: bool = True
    ):
        ml_result = self._ml_model_service.predict(
            book_id=book_id,
            prediction_type=prediction_type,
            use_cache=use_cache
        )

        saved_prediction = self._prediction_service.create_prediction(
            book_id=book_id,
            prediction_type=prediction_type,
            predicted_value=ml_result.predicted_value,
            confidence=ml_result.confidence,
            model_version=DEFAULT_MODEL_VERSION,
            metadata={"algorithm": "RandomForestClassifier"}
        )

        return ml_result, saved_prediction
