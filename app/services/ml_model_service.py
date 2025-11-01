from uuid import UUID

import numpy as np

from app.infrastructure.models.book import Book
from app.infrastructure.session_manager import get_session
from app.ml.model_loader import ml_loader


class MLModelNotLoadedError(Exception):
    pass


class BookNotFoundForMLError(Exception):
    pass


class MLPredictionResult:
    def __init__(
        self,
        book_id: str,
        book_title: str,
        predicted_value: str,
        predicted_label: str,
        confidence: float,
        features_used: dict,
        from_cache: bool
    ):
        self.book_id = book_id
        self.book_title = book_title
        self.predicted_value = predicted_value
        self.predicted_label = predicted_label
        self.confidence = confidence
        self.features_used = features_used
        self.from_cache = from_cache


class MLModelService:
    def predict(
        self,
        book_id: UUID,
        prediction_type: str,
        use_cache: bool = True
    ) -> MLPredictionResult:
        if not ml_loader.is_loaded(prediction_type):
            raise MLModelNotLoadedError(
                f"Model for '{prediction_type}' is not loaded. Please train the model first."
            )

        book_data = self._get_book_data(book_id)
        if not book_data:
            raise BookNotFoundForMLError(f"Book with id {book_id} not found")

        features_dict = self._prepare_features(book_data)
        features_array = np.array([[
            features_dict['price'],
            features_dict['category_encoded'],
            features_dict['availability_encoded']
        ]])

        prediction, confidence, from_cache = self._run_prediction(
            book_id=book_id,
            prediction_type=prediction_type,
            features_array=features_array,
            use_cache=use_cache
        )

        predicted_label = self._interpret_prediction(prediction, prediction_type)

        return MLPredictionResult(
            book_id=str(book_id),
            book_title=book_data['title'],
            predicted_value=str(prediction),
            predicted_label=predicted_label,
            confidence=round(confidence, 4),
            features_used=features_dict,
            from_cache=from_cache
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

    def _prepare_features(self, book_data: dict) -> dict:
        features = {
            'price': float(book_data['price']) if book_data['price'] else 0.0,
            'category': book_data['category'],
            'availability': book_data['availability']
        }

        features['category_encoded'] = self._encode_feature(
            'category', features['category'], self._encode_category
        )
        features['availability_encoded'] = self._encode_feature(
            'availability', features['availability'], self._encode_availability
        )

        return features

    def _encode_feature(self, feature_name: str, value: str, fallback_fn) -> int:
        encoder = ml_loader.get_encoder(feature_name)
        if encoder:
            try:
                return int(encoder.transform([value])[0])
            except ValueError:
                return fallback_fn(value)
        return fallback_fn(value)

    def _run_prediction(
        self,
        book_id: UUID,
        prediction_type: str,
        features_array: np.ndarray,
        use_cache: bool
    ) -> tuple[int, float, bool]:
        cache_key = f"{book_id}_{prediction_type}"

        if use_cache and cache_key in ml_loader._cache:
            cached = ml_loader._cache[cache_key]
            return cached['prediction'], cached['confidence'], True

        model = ml_loader.get_model(prediction_type)
        if model is None:
            raise ValueError("Model not loaded")
        
        prediction = model.predict(features_array)[0]

        if hasattr(model, 'predict_proba'):
            if model is None:
                raise ValueError("Model not loaded")
            
            proba = model.predict_proba(features_array)[0]
            confidence = float(max(proba))
        else:
            confidence = 0.85

        if use_cache:
            ml_loader._cache[cache_key] = {
                'prediction': prediction,
                'confidence': confidence
            }

        return prediction, confidence, False

    def _interpret_prediction(self, prediction: int, prediction_type: str) -> str:
        if prediction_type == 'rating':
            return "High Rating (>=4)" if prediction == 1 else "Low Rating (<4)"
        return str(prediction)

    def _encode_category(self, category: str) -> int:
        categories = {
            'Fiction': 0, 'Non-Fiction': 1, 'Mystery': 2,
            'Science Fiction': 3, 'Romance': 4, 'Fantasy': 5,
            'Thriller': 6, 'Biography': 7, 'History': 8, 'Science': 9
        }
        return categories.get(category, 0)

    def _encode_availability(self, availability: str) -> int:
        availabilities = {
            'In stock': 1, 'Out of stock': 0,
            'Available': 1, 'Not available': 0
        }
        return availabilities.get(availability, 0)
