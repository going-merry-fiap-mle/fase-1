"""
Testes para o endpoint GET /api/v1/health

Este módulo contém testes para o endpoint de verificação de saúde da API,
cobrindo cenários de sucesso e falha de conectividade com o banco de dados.
"""

from unittest.mock import patch

from app.domain.models.health_domain_model import Health


def test_health_endpoint_success(client):
    """Teste: Health check com banco conectado"""
    health_ok = Health(
        status="ok",
        message="API operacional",
        data_connectivity=True
    )

    with patch(
        "app.infrastructure.repository.health_repository.HealthRepository.check_health",
        return_value=health_ok
    ):
        response = client.get('/api/v1/health')
        assert response.status_code == 200

        data = response.get_json()
        assert 'status' in data
        assert 'message' in data
        assert 'data_connectivity' in data

        assert data['status'] == 'ok'
        assert data['message'] == 'API operacional'
        assert data['data_connectivity'] is True


def test_health_endpoint_database_error(client):
    """Teste: Health check com erro de banco de dados"""
    health_error = Health(
        status="error",
        message="Erro ao conectar com o banco: Connection refused",
        data_connectivity=False
    )

    with patch(
        "app.infrastructure.repository.health_repository.HealthRepository.check_health",
        return_value=health_error
    ):
        response = client.get('/api/v1/health')
        assert response.status_code == 200

        data = response.get_json()
        assert data['status'] == 'error'
        assert data['data_connectivity'] is False
        assert 'Erro ao conectar com o banco' in data['message']


def test_health_endpoint_response_structure(client):
    """Teste: Verificar estrutura completa da resposta"""
    health_ok = Health(
        status="ok",
        message="API operacional",
        data_connectivity=True
    )

    with patch(
        "app.infrastructure.repository.health_repository.HealthRepository.check_health",
        return_value=health_ok
    ):
        response = client.get('/api/v1/health')
        assert response.status_code == 200

        data = response.get_json()

        assert 'status' in data
        assert 'message' in data
        assert 'data_connectivity' in data

        assert isinstance(data['status'], str)
        assert isinstance(data['message'], str)
        assert isinstance(data['data_connectivity'], bool)
