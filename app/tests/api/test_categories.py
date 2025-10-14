def test_categories_endpoint(client):
    response = client.get('/api/v1/categories')
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
        category = data['items'][0]
        assert 'id' in category
        assert 'name' in category
        assert isinstance(category['id'], str)
        assert isinstance(category['name'], str)


def test_categories_endpoint_with_pagination(client):
    response = client.get('/api/v1/categories?page=1&per_page=5')
    assert response.status_code == 200

    data = response.get_json()

    assert 'items' in data
    assert 'pagination' in data

    pagination = data['pagination']
    assert pagination['page'] == 1
    assert pagination['per_page'] == 5

    assert len(data['items']) <= 5


def test_categories_endpoint_page_2(client):
    response = client.get('/api/v1/categories?page=2&per_page=3')
    assert response.status_code == 200

    data = response.get_json()

    assert 'items' in data
    assert 'pagination' in data

    assert data['pagination']['page'] == 2
    assert data['pagination']['per_page'] == 3


def test_categories_endpoint_total_calculation(client):
    response = client.get('/api/v1/categories?page=1&per_page=10')
    assert response.status_code == 200

    data = response.get_json()
    pagination = data['pagination']

    if pagination['total_items'] > 0:
        expected_pages = (pagination['total_items'] + pagination['per_page'] - 1) // pagination['per_page']
        assert pagination['total_pages'] == expected_pages

