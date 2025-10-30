from unittest.mock import patch


def test_overview_empty(client):
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_overview_stats",
        return_value={"total_books": 0, "avg_price": None, "rating_distribution": {}},
    ):
        response = client.get('/api/v1/stats/overview')
        assert response.status_code == 200

        data = response.get_json()
        assert 'total_books' in data
        assert 'avg_price' in data
        assert 'rating_distribution' in data

        assert data['total_books'] == 0
        assert data['avg_price'] is None
        assert isinstance(data['rating_distribution'], dict)


def test_overview_with_items(client):
    stats = {
        "total_books": 10,
        "avg_price": 12.34,
        "rating_distribution": {"1": 1, "2": 2, "3": 0, "4": 3, "5": 4, "unknown": 0},
    }

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_overview_stats",
        return_value=stats,
    ):
        response = client.get('/api/v1/stats/overview')
        assert response.status_code == 200

        data = response.get_json()
        assert data['total_books'] == 10
        assert isinstance(data['avg_price'], float)
        assert abs(data['avg_price'] - 12.34) < 1e-6

        rd = data['rating_distribution']
        assert isinstance(rd, dict)
        assert rd.get('1') == 1
        assert 'unknown' in rd

