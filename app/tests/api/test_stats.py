from unittest.mock import patch


def test_stats_endpoint_empty(client):
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_category_stats",
        return_value=([], 0),
    ):
        response = client.get('/api/v1/stats/categories')
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


def test_stats_endpoint_with_items(client):
    items = [
        {"name": "Ficcao", "book_count": 2, "min_price": 10.0, "max_price": 20.0, "avg_price": 15.0},
        {"name": "Ciencia", "book_count": 1, "min_price": 5.0, "max_price": 5.0, "avg_price": 5.0},
    ]

    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_category_stats",
        return_value=(items, len(items)),
    ):
        response = client.get('/api/v1/stats/categories')
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert 'pagination' in data

        assert len(data['items']) == len(items)

        first = data['items'][0]
        assert 'name' in first
        assert 'book_count' in first
        assert 'avg_price' in first
        assert isinstance(first['avg_price'], float)
        assert first['avg_price'] == round(first['avg_price'], 2)


def test_stats_pagination_params(client):
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_category_stats",
        return_value=([], 25),
    ):
        response = client.get('/api/v1/stats/categories?page=2&per_page=5')
        assert response.status_code == 200

        data = response.get_json()
        pagination = data['pagination']
        assert pagination['page'] == 2
        assert pagination['per_page'] == 5
        expected_pages = (pagination['total_items'] + pagination['per_page'] - 1) // pagination['per_page']
        assert pagination['total_pages'] == expected_pages


def test_stats_avg_price_null_when_no_books(client):
    items = [
        {"name": "Vazio", "book_count": 0, "min_price": None, "max_price": None, "avg_price": None},
    ]

    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_category_stats",
        return_value=(items, 1),
    ):
        response = client.get('/api/v1/stats/categories')
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert len(data['items']) == 1
        first = data['items'][0]
        assert first['book_count'] == 0
        assert first['avg_price'] is None

