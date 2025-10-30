"""
Testes para o endpoint GET /api/v1/categories

Este módulo contém testes abrangentes para o endpoint de listagem de categorias,
cobrindo todos os cenários possíveis incluindo validação, paginação e estrutura
de resposta.
"""

import uuid
from unittest.mock import patch

import pytest

from app.domain.models.category_domain_model import Category


@pytest.fixture
def mock_categories():
    """Categorias de exemplo para testes"""
    return [
        Category(id=uuid.UUID("c1e1e1e1-e29b-41d4-a716-446655440001"), name="Poetry"),
        Category(id=uuid.UUID("c1e1e1e1-e29b-41d4-a716-446655440002"), name="Fiction"),
        Category(id=uuid.UUID("c1e1e1e1-e29b-41d4-a716-446655440003"), name="Historical Fiction"),
    ]


def test_categories_endpoint_basic(client, mock_categories):
    """Teste: Endpoint básico sem parâmetros"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=(mock_categories, 3),
    ):
        response = client.get('/api/v1/categories')
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data
        assert isinstance(data['items'], list)
        assert len(data['items']) == 3

        pagination = data['pagination']
        assert pagination['page'] == 1
        assert pagination['per_page'] == 10
        assert pagination['total_items'] == 3
        assert pagination['total_pages'] == 1


def test_categories_endpoint_empty_list(client):
    """Teste: Lista vazia de categorias"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([], 0),
    ):
        response = client.get('/api/v1/categories')
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data
        assert len(data['items']) == 0
        assert data['pagination']['total_items'] == 0
        assert data['pagination']['total_pages'] == 0


def test_categories_endpoint_with_pagination(client, mock_categories):
    """Teste: Paginação customizada"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([mock_categories[0]], 3),
    ):
        response = client.get('/api/v1/categories?page=1&per_page=1')
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data

        pagination = data['pagination']
        assert pagination['page'] == 1
        assert pagination['per_page'] == 1
        assert pagination['total_items'] == 3
        assert pagination['total_pages'] == 3

        assert len(data['items']) == 1


def test_categories_endpoint_page_2(client, mock_categories):
    """Teste: Busca na página 2"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([mock_categories[1]], 3),
    ):
        response = client.get('/api/v1/categories?page=2&per_page=1')
        assert response.status_code == 200

        data = response.get_json()

        assert data['pagination']['page'] == 2
        assert data['pagination']['per_page'] == 1
        assert len(data['items']) == 1


def test_categories_endpoint_invalid_page_parameter(client):
    """Teste: Parâmetro page inválido (< 1)"""
    response = client.get('/api/v1/categories?page=0')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_categories_endpoint_invalid_per_page_parameter(client):
    """Teste: Parâmetro per_page inválido (> 100)"""
    response = client.get('/api/v1/categories?per_page=101')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_categories_endpoint_negative_page(client):
    """Teste: Parâmetro page negativo"""
    response = client.get('/api/v1/categories?page=-1')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_categories_endpoint_zero_per_page(client):
    """Teste: Parâmetro per_page zero"""
    response = client.get('/api/v1/categories?per_page=0')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_categories_endpoint_negative_per_page(client):
    """Teste: Parâmetro per_page negativo"""
    response = client.get('/api/v1/categories?per_page=-5')
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_categories_endpoint_large_page_number(client):
    """Teste: Número de página muito alto (sem resultados naquela página)"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([], 10),
    ):
        response = client.get('/api/v1/categories?page=100&per_page=10')
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) == 0
        assert data['pagination']['page'] == 100
        assert data['pagination']['total_items'] == 10


def test_categories_endpoint_total_calculation(client):
    """Teste: Cálculo correto de total_pages"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([], 25),
    ):
        response = client.get('/api/v1/categories?page=1&per_page=10')
        assert response.status_code == 200

        data = response.get_json()
        pagination = data['pagination']

        assert pagination['total_items'] == 25
        assert pagination['total_pages'] == 3


def test_categories_endpoint_response_structure(client, mock_categories):
    """Teste: Verificar estrutura completa da resposta"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([mock_categories[0]], 1),
    ):
        response = client.get('/api/v1/categories')
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data

        category = data['items'][0]
        assert 'id' in category
        assert 'name' in category

        assert isinstance(category['id'], str)
        assert isinstance(category['name'], str)

        pagination = data['pagination']
        assert 'page' in pagination
        assert 'per_page' in pagination
        assert 'total_items' in pagination
        assert 'total_pages' in pagination


def test_categories_endpoint_uses_items_key_for_consistency(client, mock_categories):
    """Teste: Resposta deve usar chave 'items' para consistência com outros endpoints"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([mock_categories[0]], 1),
    ):
        response = client.get('/api/v1/categories')
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert 'results' not in data


def test_categories_endpoint_custom_per_page(client, mock_categories):
    """Teste: Valor customizado de per_page"""
    with patch(
        "app.infrastructure.repository.category_repository.CategoryRepository.get_categories",
        return_value=([mock_categories[0], mock_categories[1]], 50),
    ):
        response = client.get('/api/v1/categories?per_page=2')
        assert response.status_code == 200

        data = response.get_json()
        assert data['pagination']['per_page'] == 2
        assert len(data['items']) == 2
