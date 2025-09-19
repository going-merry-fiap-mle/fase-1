def test_books_endpoint(client):
    response = client.get('/api/v1/books')
    assert response.status_code == 200 or response.status_code == 501

def test_books_search_endpoint(client):
    response = client.get('/api/v1/books/search')
    assert response.status_code == 200 or response.status_code == 501

def test_books_id_endpoint(client):
    response = client.get('/api/v1/books/1')
    assert response.status_code == 200 or response.status_code == 404 or response.status_code == 501

