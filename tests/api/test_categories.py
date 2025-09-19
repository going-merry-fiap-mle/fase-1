import pytest
from api.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_categories_endpoint(client):
    response = client.get('/api/v1/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert 'categories' in data

