from unittest.mock import patch

from app.schemas.ml_schema import FeatureOut, FeaturesResponse


def test_get_features_success_default_pagination(client):
    """Test GET /api/v1/ml/features with default pagination"""
    mock_features = FeaturesResponse(
        items=[
            FeatureOut(
                id="1",
                price_num=29.99,
                rating=4,
                availability_flag=1,
                category="Fiction",
                image_present=1,
                title="Test Book 1"
            ),
            FeatureOut(
                id="2",
                price_num=19.99,
                rating=5,
                availability_flag=1,
                category="Science",
                image_present=0,
                title="Test Book 2"
            )
        ],
        total=50,
        page=1,
        per_page=10,
        total_pages=5,
        feature_version="v1"
    )

    with patch("app.controller.ml_controller.MLController.call_controller", return_value=mock_features):
        response = client.get('/api/v1/ml/features')

        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data
        assert 'total' in data
        assert 'page' in data
        assert 'per_page' in data
        assert data['total'] == 50
        assert data['page'] == 1
        assert data['per_page'] == 10
        assert len(data['items']) == 2


def test_get_features_with_custom_pagination(client):
    """Test GET /api/v1/ml/features with custom page and per_page"""
    mock_features = FeaturesResponse(
        items=[],
        total=50,
        page=3,
        per_page=20,
        total_pages=3,
        feature_version="v1"
    )

    with patch("app.controller.ml_controller.MLController.call_controller", return_value=mock_features):
        response = client.get('/api/v1/ml/features?page=3&per_page=20')

        assert response.status_code == 200
        data = response.get_json()
        assert data['page'] == 3
        assert data['per_page'] == 20


def test_get_features_with_category_filter(client):
    """Test GET /api/v1/ml/features with category filter"""
    mock_features = FeaturesResponse(
        items=[
            FeatureOut(
                id="1",
                price_num=29.99,
                rating=4,
                availability_flag=1,
                category="Fiction",
                image_present=1,
                title="Fiction Book"
            )
        ],
        total=10,
        page=1,
        per_page=10,
        total_pages=1,
        feature_version="v1"
    )

    with patch("app.controller.ml_controller.MLController.call_controller", return_value=mock_features):
        response = client.get('/api/v1/ml/features?category=Fiction')

        assert response.status_code == 200
        data = response.get_json()
        assert data['items'][0]['category'] == 'Fiction'


def test_get_features_empty_result(client):
    """Test GET /api/v1/ml/features with no results"""
    mock_features = FeaturesResponse(
        items=[],
        total=0,
        page=1,
        per_page=10,
        total_pages=0,
        feature_version="v1"
    )

    with patch("app.controller.ml_controller.MLController.call_controller", return_value=mock_features):
        response = client.get('/api/v1/ml/features')

        assert response.status_code == 200
        data = response.get_json()
        assert data['total'] == 0
        assert len(data['items']) == 0


def test_get_features_with_page_zero(client):
    """Test GET /api/v1/ml/features with page=0"""
    mock_features = FeaturesResponse(
        items=[],
        total=0,
        page=0,
        per_page=10,
        total_pages=0,
        feature_version="v1"
    )

    with patch("app.controller.ml_controller.MLController.call_controller", return_value=mock_features):
        response = client.get('/api/v1/ml/features?page=0')

        assert response.status_code == 200


def test_get_features_internal_error(client):
    """Test GET /api/v1/ml/features with internal error"""
    with patch("app.controller.ml_controller.MLController.call_controller",
               side_effect=Exception("Database error")):
        response = client.get('/api/v1/ml/features')

        assert response.status_code == 500
        assert 'error' in response.get_json()


def test_get_manifest_success(client):
    """Test GET /api/v1/ml/manifest returns correct structure"""
    mock_manifest = {
        "features": [
            {"name": "id", "type": "string", "nullable": False},
            {"name": "price_num", "type": "float", "nullable": True},
            {"name": "rating", "type": "integer", "nullable": True},
            {"name": "availability_flag", "type": "integer", "nullable": False},
            {"name": "category", "type": "string", "nullable": False},
            {"name": "image_present", "type": "integer", "nullable": False},
            {"name": "title", "type": "string", "nullable": True}
        ],
        "version": "v1"
    }

    with patch("app.controller.ml_controller.MLController.call_manifest", return_value=mock_manifest):
        response = client.get('/api/v1/ml/manifest')

        assert response.status_code == 200
        data = response.get_json()
        assert 'features' in data
        assert 'version' in data
        assert len(data['features']) == 7
        assert data['features'][0]['name'] == 'id'


def test_get_manifest_has_required_fields(client):
    """Test GET /api/v1/ml/manifest has all required feature fields"""
    mock_manifest = {
        "features": [
            {"name": "id", "type": "string", "nullable": False},
            {"name": "price_num", "type": "float", "nullable": True}
        ],
        "version": "v1"
    }

    with patch("app.controller.ml_controller.MLController.call_manifest", return_value=mock_manifest):
        response = client.get('/api/v1/ml/manifest')

        assert response.status_code == 200
        data = response.get_json()

        for feature in data['features']:
            assert 'name' in feature
            assert 'type' in feature
            assert 'nullable' in feature


def test_get_manifest_internal_error(client):
    """Test GET /api/v1/ml/manifest with internal error"""
    with patch("app.controller.ml_controller.MLController.call_manifest",
               side_effect=Exception("Service error")):
        response = client.get('/api/v1/ml/manifest')

        assert response.status_code == 500
        assert 'error' in response.get_json()


def test_get_training_data_json_format(client):
    """Test GET /api/v1/ml/training-data with JSON format (default)"""
    mock_rows = [
        {"id": "1", "price_num": 29.99, "rating": 4, "category": "Fiction"},
        {"id": "2", "price_num": 19.99, "rating": 5, "category": "Science"}
    ]

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 2)):
        response = client.get('/api/v1/ml/training-data')

        assert response.status_code == 200
        data = response.get_json()
        assert 'rows' in data
        assert 'rows_count' in data
        assert 'total' in data
        assert 'format' in data
        assert data['format'] == 'json'
        assert data['rows_count'] == 2
        assert data['total'] == 2
        assert len(data['rows']) == 2


def test_get_training_data_with_custom_label(client):
    """Test GET /api/v1/ml/training-data with custom label"""
    mock_rows = [
        {"id": "1", "price_num": 29.99, "category": "Fiction"}
    ]

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 1)):
        response = client.get('/api/v1/ml/training-data?label=category')

        assert response.status_code == 200
        data = response.get_json()
        assert data['format'] == 'json'


def test_get_training_data_with_sample(client):
    """Test GET /api/v1/ml/training-data with sample parameter"""
    mock_rows = [
        {"id": "1", "price_num": 29.99, "rating": 4}
    ]

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 1)):
        response = client.get('/api/v1/ml/training-data?sample=0.5')

        assert response.status_code == 200
        data = response.get_json()
        assert 'rows' in data


def test_get_training_data_with_seed(client):
    """Test GET /api/v1/ml/training-data with seed parameter"""
    mock_rows = [
        {"id": "1", "price_num": 29.99, "rating": 4}
    ]

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 1)):
        response = client.get('/api/v1/ml/training-data?seed=42')

        assert response.status_code == 200
        data = response.get_json()
        assert 'rows' in data


def test_get_training_data_csv_format(client):
    """Test GET /api/v1/ml/training-data with CSV format"""
    mock_rows = [
        {"id": "1", "price_num": 29.99, "rating": 4, "category": "Fiction"},
        {"id": "2", "price_num": 19.99, "rating": 5, "category": "Science"}
    ]

    mock_manifest = {
        "features": [
            {"name": "id", "type": "string", "nullable": False},
            {"name": "price_num", "type": "float", "nullable": True},
            {"name": "category", "type": "string", "nullable": False}
        ]
    }

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 2)), \
         patch("app.controller.ml_controller.MLController.call_manifest", return_value=mock_manifest):

        response = client.get('/api/v1/ml/training-data?format=csv')

        assert response.status_code == 200
        assert response.content_type == 'text/csv; charset=utf-8'
        assert 'Content-Disposition' in response.headers
        assert 'training_data.csv' in response.headers['Content-Disposition']

        csv_data = response.get_data(as_text=True)
        assert 'id' in csv_data
        assert 'price_num' in csv_data
        assert 'category' in csv_data


def test_get_training_data_invalid_format(client):
    """Test GET /api/v1/ml/training-data with invalid format"""
    mock_rows = []

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 0)):
        response = client.get('/api/v1/ml/training-data?format=xml')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid format' in data['error']


def test_get_training_data_value_error(client):
    """Test GET /api/v1/ml/training-data with ValueError from controller"""
    with patch("app.controller.ml_controller.MLController.call_training_data",
               side_effect=ValueError("Label 'invalid_label' not found")):
        response = client.get('/api/v1/ml/training-data?label=invalid_label')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'invalid_label' in data['error']


def test_get_training_data_empty_result(client):
    """Test GET /api/v1/ml/training-data with no data"""
    mock_rows = []

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 0)):
        response = client.get('/api/v1/ml/training-data')

        assert response.status_code == 200
        data = response.get_json()
        assert data['rows_count'] == 0
        assert data['total'] == 0
        assert len(data['rows']) == 0


def test_get_training_data_internal_error(client):
    """Test GET /api/v1/ml/training-data with internal error"""
    with patch("app.controller.ml_controller.MLController.call_training_data",
               side_effect=Exception("Database connection error")):
        response = client.get('/api/v1/ml/training-data')

        assert response.status_code == 500
        assert 'error' in response.get_json()


def test_get_training_data_csv_with_custom_label(client):
    """Test GET /api/v1/ml/training-data CSV format with custom label not in manifest"""
    mock_rows = [
        {"id": "1", "price_num": 29.99, "custom_label": "test"}
    ]

    mock_manifest = {
        "features": [
            {"name": "id", "type": "string", "nullable": False},
            {"name": "price_num", "type": "float", "nullable": True}
        ]
    }

    with patch("app.controller.ml_controller.MLController.call_training_data", return_value=(mock_rows, 1)), \
         patch("app.controller.ml_controller.MLController.call_manifest", return_value=mock_manifest):

        response = client.get('/api/v1/ml/training-data?format=csv&label=custom_label')

        assert response.status_code == 200
        csv_data = response.get_data(as_text=True)
        assert 'custom_label' in csv_data
