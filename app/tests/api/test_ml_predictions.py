from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

from app.domain.models.prediction_domain_model import Prediction
from app.services.ml_model_service import (
    BookNotFoundForMLError,
    MLModelNotLoadedError,
    MLPredictionResult
)


def test_create_prediction_success(client):
    book_id = uuid4()
    prediction_id = uuid4()

    prediction_domain = Prediction(
        id=prediction_id,
        book_id=book_id,
        prediction_type="rating",
        predicted_value="5",
        confidence=0.95,
        model_version="v1.0.0",
        metadata={"algorithm": "random_forest"},
        created_at=datetime.now()
    )

    mock_book_data = {
        'title': 'Test Book',
        'price': 29.99,
        'category': 'Fiction',
        'availability': 'In stock'
    }

    with patch(
        "app.infrastructure.repository.prediction_repository.PredictionRepository.create_prediction",
        return_value=prediction_domain
    ), patch(
        "app.controller.ml.create_prediction_controller.CreatePredictionController._get_book_data",
        return_value=mock_book_data
    ):
        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating",
                "predicted_value": "5",
                "confidence": 0.95,
                "model_version": "v1.0.0",
                "metadata": {"algorithm": "random_forest"}
            }
        )

        assert response.status_code == 201
        data = response.get_json()
        assert 'prediction' in data
        assert 'saved_prediction_id' in data
        assert data['prediction']['predicted_value'] == '5'
        assert data['prediction']['confidence'] == 0.95
        assert data['prediction']['model_version'] == 'v1.0.0'
        assert data['prediction']['book_title'] == 'Test Book'


def test_create_prediction_without_metadata(client):
    book_id = uuid4()
    prediction_id = uuid4()

    prediction_domain = Prediction(
        id=prediction_id,
        book_id=book_id,
        prediction_type="category",
        predicted_value="Fiction",
        confidence=0.87,
        model_version="v2.0.0",
        metadata=None,
        created_at=datetime.now()
    )

    mock_book_data = {
        'title': 'Test Book',
        'price': 29.99,
        'category': 'Fiction',
        'availability': 'In stock'
    }

    with patch(
        "app.infrastructure.repository.prediction_repository.PredictionRepository.create_prediction",
        return_value=prediction_domain
    ), patch(
        "app.controller.ml.create_prediction_controller.CreatePredictionController._get_book_data",
        return_value=mock_book_data
    ):
        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "category",
                "predicted_value": "Fiction",
                "confidence": 0.87,
                "model_version": "v2.0.0"
            }
        )

        assert response.status_code == 201
        data = response.get_json()
        assert 'prediction' in data
        assert 'saved_prediction_id' in data


def test_create_prediction_missing_required_field(client):
    response = client.post(
        '/api/v1/ml/predictions',
        json={
            "book_id": str(uuid4()),
            "prediction_type": "rating",
            "predicted_value": "5",
            "confidence": 0.95,
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'


def test_create_prediction_invalid_prediction_type(client):
    response = client.post(
        '/api/v1/ml/predictions',
        json={
            "book_id": str(uuid4()),
            "prediction_type": "invalid_type",
            "predicted_value": "5",
            "confidence": 0.95,
            "model_version": "v1.0.0"
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_create_prediction_confidence_out_of_range(client):
    response = client.post(
        '/api/v1/ml/predictions',
        json={
            "book_id": str(uuid4()),
            "prediction_type": "rating",
            "predicted_value": "5",
            "confidence": 1.5,
            "model_version": "v1.0.0"
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_create_prediction_confidence_boundaries(client):
    book_id = uuid4()
    prediction_id = uuid4()
    prediction_domain = Prediction(
        id=prediction_id,
        book_id=book_id,
        prediction_type="rating",
        predicted_value="1",
        confidence=0.0,
        model_version="v1.0.0",
        metadata=None,
        created_at=datetime.now()
    )

    mock_book_data = {
        'title': 'Test Book',
        'price': 29.99,
        'category': 'Fiction',
        'availability': 'In stock'
    }

    with patch(
        "app.infrastructure.repository.prediction_repository.PredictionRepository.create_prediction",
        return_value=prediction_domain
    ), patch(
        "app.controller.ml.create_prediction_controller.CreatePredictionController._get_book_data",
        return_value=mock_book_data
    ):
        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating",
                "predicted_value": "1",
                "confidence": 0.0,
                "model_version": "v1.0.0"
            }
        )

        assert response.status_code == 201
        assert response.get_json()['prediction']['confidence'] == 0.0

    prediction_domain.confidence = 1.0
    with patch(
        "app.infrastructure.repository.prediction_repository.PredictionRepository.create_prediction",
        return_value=prediction_domain
    ), patch(
        "app.controller.ml.create_prediction_controller.CreatePredictionController._get_book_data",
        return_value=mock_book_data
    ):
        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating",
                "predicted_value": "5",
                "confidence": 1.0,
                "model_version": "v1.0.0"
            }
        )

        assert response.status_code == 201
        assert response.get_json()['prediction']['confidence'] == 1.0

    response = client.post(
        '/api/v1/ml/predictions',
        json={
            "book_id": str(book_id),
            "prediction_type": "rating",
            "predicted_value": "5",
            "confidence": -0.1,
            "model_version": "v1.0.0"
        }
    )

    assert response.status_code == 400


def test_create_prediction_book_not_found(client):
    book_id = uuid4()

    with patch(
        "app.controller.ml.create_prediction_controller.CreatePredictionController._get_book_data",
        return_value=None
    ):
        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating",
                "predicted_value": "5",
                "confidence": 0.95,
                "model_version": "v1.0.0"
            }
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Book not found'


def test_create_prediction_invalid_uuid(client):
    response = client.post(
        '/api/v1/ml/predictions',
        json={
            "book_id": "invalid-uuid",
            "prediction_type": "rating",
            "predicted_value": "5",
            "confidence": 0.95,
            "model_version": "v1.0.0"
        }
    )

    assert response.status_code == 400


def test_create_prediction_empty_body(client):
    response = client.post('/api/v1/ml/predictions')
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_create_prediction_all_prediction_types(client):
    prediction_types = ['rating', 'category', 'price', 'recommendation']
    book_id = uuid4()

    mock_book_data = {
        'title': 'Test Book',
        'price': 29.99,
        'category': 'Fiction',
        'availability': 'In stock'
    }

    for pred_type in prediction_types:
        prediction_id = uuid4()
        prediction_domain = Prediction(
            id=prediction_id,
            book_id=book_id,
            prediction_type=pred_type,
            predicted_value="test_value",
            confidence=0.90,
            model_version="v1.0.0",
            metadata=None,
            created_at=datetime.now()
        )

        with patch(
            "app.infrastructure.repository.prediction_repository.PredictionRepository.create_prediction",
            return_value=prediction_domain
        ), patch(
            "app.controller.ml.create_prediction_controller.CreatePredictionController._get_book_data",
            return_value=mock_book_data
        ):
            response = client.post(
                '/api/v1/ml/predictions',
                json={
                    "book_id": str(book_id),
                    "prediction_type": pred_type,
                    "predicted_value": "test_value",
                    "confidence": 0.90,
                    "model_version": "v1.0.0"
                }
            )

            assert response.status_code == 201
            data = response.get_json()
            assert 'prediction' in data
            assert data['prediction']['predicted_value'] == "test_value"


def test_create_prediction_internal_server_error(client):
    mock_book_data = {
        'title': 'Test Book',
        'price': 29.99,
        'category': 'Fiction',
        'availability': 'In stock'
    }

    with patch(
        "app.infrastructure.repository.prediction_repository.PredictionRepository.create_prediction",
        side_effect=Exception("Database connection error")
    ), patch(
        "app.controller.ml.create_prediction_controller.CreatePredictionController._get_book_data",
        return_value=mock_book_data
    ):
        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(uuid4()),
                "prediction_type": "rating",
                "predicted_value": "5",
                "confidence": 0.95,
                "model_version": "v1.0.0"
            }
        )

        assert response.status_code == 500
        assert response.get_json()['error'] == 'Internal server error'


def test_execute_ml_prediction_success(client):
    book_id = uuid4()

    ml_result = MLPredictionResult(
        book_id=str(book_id),
        book_title="Test Book",
        predicted_value="1",
        predicted_label="High Rating (>=4)",
        confidence=0.85,
        features_used={"price": 29.99, "category": "Fiction"},
        from_cache=False
    )

    mock_prediction_domain = MagicMock()
    mock_prediction_domain.id = uuid4()
    mock_prediction_domain.model_version = "v1.0.0"

    with patch("app.services.ml_model_service.MLModelService.predict", return_value=ml_result), \
         patch("app.services.prediction_service.PredictionService.create_prediction", return_value=mock_prediction_domain):

        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating"
            }
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'prediction' in data
        assert 'saved_prediction_id' in data
        assert data['prediction']['book_id'] == str(book_id)


def test_execute_ml_prediction_with_cache(client):
    book_id = uuid4()

    ml_result = MLPredictionResult(
        book_id=str(book_id),
        book_title="Cached Book",
        predicted_value="1",
        predicted_label="High Rating (>=4)",
        confidence=0.90,
        features_used={"price": 19.99},
        from_cache=True
    )

    mock_prediction_domain = MagicMock()
    mock_prediction_domain.id = uuid4()
    mock_prediction_domain.model_version = "v1.0.0"

    with patch("app.services.ml_model_service.MLModelService.predict", return_value=ml_result), \
         patch("app.services.prediction_service.PredictionService.create_prediction", return_value=mock_prediction_domain):

        response = client.post(
            '/api/v1/ml/predictions?use_cache=true',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating"
            }
        )

        assert response.status_code == 200
        assert response.get_json()['prediction']['from_cache'] is True


def test_execute_ml_prediction_model_not_loaded(client):
    book_id = uuid4()

    with patch("app.services.ml_model_service.MLModelService.predict",
               side_effect=MLModelNotLoadedError("Model for 'rating' is not loaded")):

        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating"
            }
        )

        assert response.status_code == 503
        data = response.get_json()
        assert data['error'] == 'Model not available'


def test_execute_ml_prediction_book_not_found(client):
    book_id = uuid4()

    with patch("app.services.ml_model_service.MLModelService.predict",
               side_effect=BookNotFoundForMLError(f"Book with id {book_id} not found")):

        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating"
            }
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Book not found'


def test_execute_ml_prediction_invalid_book_id(client):
    response = client.post(
        '/api/v1/ml/predictions',
        json={
            "book_id": "not-a-uuid",
            "prediction_type": "rating"
        }
    )

    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_execute_ml_prediction_missing_prediction_type(client):
    response = client.post(
        '/api/v1/ml/predictions',
        json={
            "book_id": str(uuid4())
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid parameters'


def test_execute_ml_prediction_internal_error(client):
    book_id = uuid4()

    with patch("app.services.ml_model_service.MLModelService.predict",
               side_effect=Exception("Unexpected error")):

        response = client.post(
            '/api/v1/ml/predictions',
            json={
                "book_id": str(book_id),
                "prediction_type": "rating"
            }
        )

        assert response.status_code == 500
        assert response.get_json()['error'] == 'Internal server error'


def test_http_method_get_not_allowed(client):
    response = client.get('/api/v1/ml/predictions')
    assert response.status_code == 500
    assert 'error' in response.get_json()


def test_http_method_put_not_allowed(client):
    response = client.put('/api/v1/ml/predictions', json={})
    assert response.status_code == 500
    assert 'error' in response.get_json()


def test_http_method_delete_not_allowed(client):
    response = client.delete('/api/v1/ml/predictions')
    assert response.status_code == 500
    assert 'error' in response.get_json()
