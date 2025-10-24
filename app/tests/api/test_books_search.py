"""
Testes para o endpoint GET /api/v1/books/search

Este módulo contém testes abrangentes para o endpoint de busca de livros,
cobrindo todos os cenários possíveis incluindo validação, paginação e diferentes
combinações de parâmetros de busca.
"""

import uuid
from decimal import Decimal
from unittest.mock import patch

import pytest

from app.domain.models.book_domain_model import Book
from app.domain.models.category_domain_model import Category


# Fixtures para dados de teste
@pytest.fixture
def mock_category_fiction():
    """Categoria Fiction para testes"""
    return Category(id=uuid.uuid4(), name="Fiction")


@pytest.fixture
def mock_category_poetry():
    """Categoria Poetry para testes"""
    return Category(id=uuid.uuid4(), name="Poetry")


@pytest.fixture
def mock_books(mock_category_fiction, mock_category_poetry):
    """Livros de exemplo para testes"""
    return [
        Book(
            id=uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),
            title="Python Programming",
            price=Decimal("29.99"),
            rating=4,
            availability="In stock",
            category=mock_category_fiction,
            image_url="https://example.com/python.jpg",
        ),
        Book(
            id=uuid.UUID("550e8400-e29b-41d4-a716-446655440002"),
            title="Data Science with Python",
            price=Decimal("39.99"),
            rating=5,
            availability="In stock",
            category=mock_category_fiction,
            image_url="https://example.com/datascience.jpg",
        ),
        Book(
            id=uuid.UUID("550e8400-e29b-41d4-a716-446655440003"),
            title="A Light in the Attic",
            price=Decimal("51.77"),
            rating=3,
            availability="In stock",
            category=mock_category_poetry,
            image_url="https://example.com/light.jpg",
        ),
    ]


# Testes de validação de parâmetros


def test_books_search_without_parameters_returns_400(client):
    """Teste: Busca sem parâmetros deve retornar erro 400"""
    response = client.get("/api/v1/books/search")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid parameters'
    assert 'message' in data
    assert 'At least one search parameter' in data['message']


def test_books_search_empty_string_title(client):
    """Teste: Busca com título vazio deve retornar erro 400"""
    response = client.get("/api/v1/books/search?title=")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_search_empty_string_category(client):
    """Teste: Busca com categoria vazia deve retornar erro 400"""
    response = client.get("/api/v1/books/search?category=")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_search_whitespace_only_title(client):
    """Teste: Busca com título contendo apenas espaços deve retornar erro 400"""
    response = client.get("/api/v1/books/search?title=%20%20%20")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_search_whitespace_only_category(client):
    """Teste: Busca com categoria contendo apenas espaços deve retornar erro 400"""
    response = client.get("/api/v1/books/search?category=%20%20%20")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


# Testes de funcionalidade de busca


def test_books_search_by_title_only(client, mock_books):
    """Teste: Busca apenas por título"""
    python_books = [mock_books[0], mock_books[1]]  # 2 livros com "Python" no título

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=(python_books, 2),
    ):
        response = client.get("/api/v1/books/search?title=Python")
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert 'pagination' in data
        assert isinstance(data['items'], list)
        assert len(data['items']) == 2

        for book in data['items']:
            assert 'Python' in book['title']

        pagination = data['pagination']
        assert pagination['page'] == 1
        assert pagination['per_page'] == 10
        assert pagination['total_items'] == 2
        assert pagination['total_pages'] == 1


def test_books_search_by_category_only(client, mock_books):
    """Teste: Busca apenas por categoria"""
    fiction_books = [mock_books[0], mock_books[1]]  # 2 livros de Fiction

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=(fiction_books, 2),
    ):
        response = client.get("/api/v1/books/search?category=Fiction")
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert len(data['items']) == 2

        for book in data['items']:
            assert book['category'] == 'Fiction'


def test_books_search_by_title_and_category(client, mock_books):
    """Teste: Busca por título E categoria (AND logic)"""
    filtered_books = [mock_books[0]]  # Apenas 1 livro com "Python" E categoria "Fiction"

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=(filtered_books, 1),
    ):
        response = client.get("/api/v1/books/search?title=Python&category=Fiction")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) == 1
        assert 'Python' in data['items'][0]['title']
        assert data['items'][0]['category'] == 'Fiction'


def test_books_search_case_insensitive(client, mock_books):
    """Teste: Busca case-insensitive"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([mock_books[0]], 1),
    ):
        response = client.get("/api/v1/books/search?title=python")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) > 0


def test_books_search_partial_match(client, mock_books):
    """Teste: Busca por correspondência parcial"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([mock_books[0]], 1),
    ):
        response = client.get("/api/v1/books/search?title=Pyth")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) > 0


def test_books_search_with_special_characters(client, mock_books):
    """Teste: Busca com caracteres especiais"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([mock_books[0]], 1),
    ):
        response = client.get("/api/v1/books/search?title=C%2B%2B")
        assert response.status_code == 200


# Testes de resultados


def test_books_search_no_results(client):
    """Teste: Busca que não retorna resultados"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([], 0),
    ):
        response = client.get("/api/v1/books/search?title=NonExistentBook")
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert len(data['items']) == 0
        assert data['pagination']['total_items'] == 0
        assert data['pagination']['total_pages'] == 0


# Testes de paginação


def test_books_search_with_pagination(client, mock_books):
    """Teste: Busca com paginação"""
    first_page_books = [mock_books[0]]

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=(first_page_books, 3),
    ):
        response = client.get("/api/v1/books/search?title=Python&page=1&per_page=1")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) == 1
        assert data['pagination']['page'] == 1
        assert data['pagination']['per_page'] == 1
        assert data['pagination']['total_items'] == 3
        assert data['pagination']['total_pages'] == 3


def test_books_search_page_2(client, mock_books):
    """Teste: Busca na página 2"""
    second_page_books = [mock_books[1]]

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=(second_page_books, 3),
    ):
        response = client.get("/api/v1/books/search?title=Python&page=2&per_page=1")
        assert response.status_code == 200

        data = response.get_json()
        assert data['pagination']['page'] == 2
        assert len(data['items']) == 1


def test_books_search_invalid_page_parameter(client):
    """Teste: Parâmetro page inválido (< 1)"""
    response = client.get("/api/v1/books/search?title=Python&page=0")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_search_invalid_per_page_parameter(client):
    """Teste: Parâmetro per_page inválido (> 100)"""
    response = client.get("/api/v1/books/search?title=Python&per_page=101")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_search_negative_page(client):
    """Teste: Parâmetro page negativo"""
    response = client.get("/api/v1/books/search?title=Python&page=-1")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_search_zero_per_page(client):
    """Teste: Parâmetro per_page zero"""
    response = client.get("/api/v1/books/search?title=Python&per_page=0")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_search_large_page_number(client, mock_books):
    """Teste: Número de página muito alto (sem resultados naquela página)"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([], 10),
    ):
        response = client.get("/api/v1/books/search?title=Python&page=100&per_page=10")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) == 0
        assert data['pagination']['page'] == 100
        assert data['pagination']['total_items'] == 10


def test_books_search_custom_per_page(client, mock_books):
    """Teste: Valor customizado de per_page"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([mock_books[0], mock_books[1]], 50),
    ):
        response = client.get("/api/v1/books/search?title=Python&per_page=2")
        assert response.status_code == 200

        data = response.get_json()
        assert data['pagination']['per_page'] == 2
        assert len(data['items']) == 2


# Testes de estrutura de resposta


def test_books_search_response_structure(client, mock_books):
    """Teste: Verificar estrutura completa da resposta"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([mock_books[0]], 1),
    ):
        response = client.get("/api/v1/books/search?title=Python")
        assert response.status_code == 200

        data = response.get_json()

        assert 'items' in data
        assert 'pagination' in data

        book = data['items'][0]
        assert 'id' in book
        assert 'title' in book
        assert 'price' in book
        assert 'rating' in book
        assert 'availability' in book
        assert 'category' in book
        assert 'image_url' in book

        # Verifica tipos
        assert isinstance(book['id'], str)
        assert isinstance(book['title'], str)
        assert isinstance(book['price'], str)
        assert isinstance(book['rating'], int)
        assert isinstance(book['availability'], str)
        assert isinstance(book['category'], str)
        assert isinstance(book['image_url'], str)

        pagination = data['pagination']
        assert 'page' in pagination
        assert 'per_page' in pagination
        assert 'total_items' in pagination
        assert 'total_pages' in pagination


def test_books_search_uses_items_key_for_consistency(client, mock_books):
    """Teste: Resposta deve usar chave 'items' para consistência com outros endpoints"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.search_books",
        return_value=([mock_books[0]], 1),
    ):
        response = client.get("/api/v1/books/search?title=Python")
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert 'results' not in data
