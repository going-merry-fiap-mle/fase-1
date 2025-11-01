from uuid import UUID

from app.infrastructure.adapters.prediction_adapter import PredictionAdapter
from app.schemas.ml_schema import MLExecutionResponse, MLPredictionResponse
from app.services.ml_model_service import MLModelService
from app.services.prediction_service import PredictionService
from app.usecases.ml.execute_prediction_use_case import ExecutePredictionUseCase


class ExecutePredictionController:
    def call_controller(
        self,
        book_id: UUID,
        prediction_type: str,
        use_cache: bool = True
    ) -> MLExecutionResponse:
        ml_model_service = MLModelService()
        prediction_adapter = PredictionAdapter()
        prediction_service = PredictionService(prediction_adapter)
        use_case = ExecutePredictionUseCase(ml_model_service, prediction_service)

        ml_result, saved_prediction = use_case.execute(
            book_id=book_id,
            prediction_type=prediction_type,
            use_cache=use_cache
        )

        prediction_response = MLPredictionResponse(
            book_id=ml_result.book_id,
            book_title=ml_result.book_title,
            predicted_value=ml_result.predicted_value,
            predicted_label=ml_result.predicted_label,
            confidence=ml_result.confidence,
            features_used=ml_result.features_used,
            model_version=saved_prediction.model_version,
            from_cache=ml_result.from_cache
        )

        return MLExecutionResponse(
            prediction=prediction_response,
            saved_prediction_id=str(saved_prediction.id)
        )
