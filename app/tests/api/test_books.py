from unittest.mock import patch
import pytest
from app.core.security import create_access_token


@pytest.fixture
def auth_headers():
    token = create_access_token(data={"sub": "admin"})
    return {"Authorization": f"Bearer {token}"}

def test_books_endpoint(client, auth_headers):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_books",
        return_value=([], 0),
    ):
        response = client.get("/api/v1/books", headers=auth_headers)
        assert response.status_code == 200 or response.status_code == 501


def test_books_search_endpoint(client):
    response = client.get("/api/v1/books/search")
    assert response.status_code == 200 or response.status_code == 501


def test_books_id_endpoint(client, auth_headers):
    valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
    response = client.get(f"/api/v1/books/{valid_uuid}", headers=auth_headers)
    assert (
        response.status_code == 200
        or response.status_code == 404
        or response.status_code == 501
    )


def test_books_id_endpoint_invalid_uuid(client, auth_headers):
    response = client.get("/api/v1/books/invalid-uuid", headers=auth_headers)
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid value'
    assert 'message' in data


def test_books_id_endpoint_integer_not_accepted(client, auth_headers):
    response = client.get("/api/v1/books/123", headers=auth_headers)
    assert response.status_code == 400


def test_books_endpoint_without_auth(client):
    response = client.get("/api/v1/books")
    assert response.status_code == 401
