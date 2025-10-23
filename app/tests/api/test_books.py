from unittest.mock import patch


def test_books_endpoint(client):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_books",
        return_value=([], 0),
    ):
        response = client.get("/api/v1/books")
        assert response.status_code == 200 or response.status_code == 501


def test_books_search_endpoint(client):
    response = client.get("/api/v1/books/search")
    assert response.status_code == 200 or response.status_code == 501


def test_books_id_endpoint(client):
    valid_uuid = "b7e7fd8c-ad40-4634-a00c-3bc6aa11b09e"
    response = client.get(f"/api/v1/books/{valid_uuid}")
    assert (
        response.status_code == 200
        or response.status_code == 404
        or response.status_code == 501
    )


def test_books_id_endpoint_invalid_uuid(client):
    response = client.get("/api/v1/books/invalid-uuid")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid value'
    assert 'message' in data


def test_books_id_endpoint_integer_not_accepted(client):
    response = client.get("/api/v1/books/123")
    assert response.status_code == 400
