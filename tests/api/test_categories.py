def test_categories_endpoint(client):
    response = client.get('/api/v1/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert 'categories' in data

