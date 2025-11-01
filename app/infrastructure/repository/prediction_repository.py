from uuid import UUID

from app.domain.models.prediction_domain_model import Prediction as PredictionDomain
from app.infrastructure.models.prediction import Prediction
from app.infrastructure.session_manager import get_session
from app.port.prediction_port import IPredictionRepository


class PredictionRepository(IPredictionRepository):

    def create_prediction(
        self,
        book_id: UUID,
        prediction_type: str,
        predicted_value: str,
        confidence: float,
        model_version: str,
        metadata: dict | None = None
    ) -> PredictionDomain:
        with get_session() as session:
            prediction_db = Prediction(
                book_id=book_id,
                prediction_type=prediction_type,
                predicted_value=predicted_value,
                confidence=confidence,
                model_version=model_version,
                prediction_metadata=metadata,
            )

            session.add(prediction_db)
            session.flush()

            return prediction_db.to_domain()
