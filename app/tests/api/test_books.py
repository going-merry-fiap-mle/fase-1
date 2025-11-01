from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch
from uuid import UUID


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
    
    valid_uuid = "b7e7fd8c-ad40-4634-a00c-3bc6aa11b09e"
    
    category = SimpleNamespace(name="Fiction")
    
    book = SimpleNamespace(
        id=UUID(valid_uuid),
        title="Title",
        price=Decimal("9.99"),
        rating=4,
        availability="In stock",
        category=category,
        image_url="http://example.com/img.jpg",
    )

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_book_by_id",
        return_value=book,
    ):

        response = client.get(f"/api/v1/books/{valid_uuid}")
        assert (
            response.status_code == 200
        )

def test_books_id_endpoint_book_not_found(client):

    valid_uuid = "b7e7fd8c-ad40-4634-a00c-3bc6aa11b09e"

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_book_by_id",
        return_value=None,
    ):

        response = client.get(f"/api/v1/books/{valid_uuid}")
        assert (
            response.status_code == 404
        )

def test_books_id_endpoint_invalid_uuid(client):
    response = client.get("/api/v1/books/invalid-uuid")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'
    assert 'message' in data


def test_books_id_endpoint_integer_not_accepted(client):
    response = client.get("/api/v1/books/123")
    assert response.status_code == 400


def test_price_range_missing_params(client):
    response = client.get("/api/v1/books/price-range")
    assert response.status_code == 400

def test_price_range_missing_params_data(client):
    response = client.get("/api/v1/books/price-range")
    data = response.get_json()
    assert data is not None

def test_price_range_invalid_number_param(client):
    # non-numeric min should result in invalid parameters (400) or server error if Decimal handling differs
    response = client.get("/api/v1/books/price-range?min=abc&max=10")
    assert response.status_code == 400

def test_books_by_price_endpoint(client):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_books_by_price",
        return_value=([], 0),
    ):
        response = client.get("/api/v1/books/price-range?min=50&max=60")
        assert response.status_code == 200

def test_price_range_min_less_than_max(client):
    response = client.get("/api/v1/books/price-range?min=50&max=10")
    assert response.status_code == 400