def test_health_endpoint(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'message' in data
    assert 'data_connectivity' in data
    # Verifica que conectividade está OK
    assert data['data_connectivity'] is True
    assert data['status'] == 'ok'
    assert 'API operacional' in data['message']
