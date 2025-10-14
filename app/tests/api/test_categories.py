def test_categories_endpoint(client):
    response = client.get('/api/v1/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert 'categories' in data
    assert isinstance(data['categories'], list)

    # Verifica se retornou categorias
    if len(data['categories']) > 0:
        # Verifica a estrutura de cada categoria
        category = data['categories'][0]
        assert 'name' in category
        assert isinstance(category['name'], str)

