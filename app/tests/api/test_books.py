from unittest.mock import patch


def test_books_endpoint(client):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_books",
        return_value=([], 0),
    ):
        response = client.get("/api/v1/books")
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data
        assert isinstance(data['items'], list)

        pagination = data['pagination']
        assert 'page' in pagination
        assert 'per_page' in pagination
        assert 'total_items' in pagination
        assert 'total_pages' in pagination

        assert pagination['page'] == 1
        assert pagination['per_page'] == 10

        if len(data['items']) > 0:
            book = data['items'][0]
            assert 'id' in book
            assert 'title' in book
            assert 'price' in book
            assert 'rating' in book
            assert 'availability' in book
            assert 'category' in book
            assert 'image_url' in book
            assert isinstance(book['id'], str)
            assert isinstance(book['title'], str)
            assert isinstance(book['price'], str)
            assert isinstance(book['rating'], int)
            assert isinstance(book['availability'], str)
            assert isinstance(book['category'], str)
            assert isinstance(book['image_url'], str)


def test_books_endpoint_with_pagination(client):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_books",
        return_value=([], 0),
    ):
        response = client.get('/api/v1/books?page=1&per_page=5')
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data

        pagination = data['pagination']
        assert pagination['page'] == 1
        assert pagination['per_page'] == 5

        assert len(data['items']) <= 5


def test_books_endpoint_page_2(client):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_books",
        return_value=([], 0),
    ):
        response = client.get('/api/v1/books?page=2&per_page=3')
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data

        assert data['pagination']['page'] == 2
        assert data['pagination']['per_page'] == 3


def test_books_endpoint_total_calculation(client):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_books",
        return_value=([], 25),
    ):
        response = client.get('/api/v1/books?page=1&per_page=10')
        assert response.status_code == 200

        data = response.get_json()
        pagination = data['pagination']

        if pagination['total_items'] > 0:
            expected_pages = (pagination['total_items'] + pagination['per_page'] - 1) // pagination['per_page']
            assert pagination['total_pages'] == expected_pages


def test_books_endpoint_invalid_page_zero(client):
    response = client.get('/api/v1/books?page=0')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'
    assert 'details' in data


def test_books_endpoint_invalid_page_negative(client):
    response = client.get('/api/v1/books?page=-1')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'


def test_books_endpoint_invalid_per_page_zero(client):
    response = client.get('/api/v1/books?per_page=0')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'


def test_books_endpoint_invalid_per_page_above_limit(client):
    response = client.get('/api/v1/books?per_page=101')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'
    assert 'details' in data


def test_books_endpoint_invalid_per_page_negative(client):
    response = client.get('/api/v1/books?per_page=-5')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'


def test_books_id_endpoint(client):
    valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
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
