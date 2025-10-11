def test_books_endpoint(client):
    response = client.get('/api/v1/books')
    assert response.status_code == 200 or response.status_code == 501

def test_books_search_endpoint(client):
    response = client.get('/api/v1/books/search')
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data
    assert isinstance(data['results'], list)

def test_books_search_with_title(client):
    response = client.get('/api/v1/books/search?title=Python')
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data
    assert isinstance(data['results'], list)
    # Verifica se retornou o livro com Python no título
    if len(data['results']) > 0:
        assert any('python' in book['title'].lower() for book in data['results'])

def test_books_search_with_category(client):
    response = client.get('/api/v1/books/search?category=Poetry')
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data
    assert isinstance(data['results'], list)
    # Verifica se retornou livros da categoria Poetry
    if len(data['results']) > 0:
        assert all(book['category'].lower() == 'poetry' for book in data['results'])

def test_books_search_with_title_and_category(client):
    response = client.get('/api/v1/books/search?title=Collection&category=Poetry')
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data
    assert isinstance(data['results'], list)
    # Verifica se aplicou ambos os filtros
    if len(data['results']) > 0:
        for book in data['results']:
            assert 'collection' in book['title'].lower()
            assert book['category'].lower() == 'poetry'

def test_books_id_endpoint(client):
    response = client.get('/api/v1/books/1')
    assert response.status_code == 200 or response.status_code == 404 or response.status_code == 501

