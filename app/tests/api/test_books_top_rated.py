"""
Testes para o endpoint GET /api/v1/books/top-rated

Este módulo contém testes abrangentes para o endpoint de livros com maiores avaliações,
cobrindo todos os cenários possíveis incluindo validação, paginação e ordenação.
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
def mock_books_sorted_by_rating(mock_category_fiction, mock_category_poetry):
    """Livros ordenados por rating (maior para menor)"""
    return [
        Book(
            id=uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),
            title="Advanced Python",
            price=Decimal("49.99"),
            rating=5,
            availability="In stock",
            category=mock_category_fiction,
            image_url="https://example.com/advanced_python.jpg",
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
            title="Python for Beginners",
            price=Decimal("29.99"),
            rating=4,
            availability="In stock",
            category=mock_category_fiction,
            image_url="https://example.com/python_beginners.jpg",
        ),
        Book(
            id=uuid.UUID("550e8400-e29b-41d4-a716-446655440004"),
            title="A Light in the Attic",
            price=Decimal("51.77"),
            rating=3,
            availability="In stock",
            category=mock_category_poetry,
            image_url="https://example.com/light.jpg",
        ),
    ]


# Testes de funcionalidade básica


def test_books_top_rated_basic_success(client, mock_books_sorted_by_rating):
    """Teste: Buscar livros com maiores avaliações - sucesso básico"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=(mock_books_sorted_by_rating, 4),
    ):
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert 'pagination' in data
        assert isinstance(data['items'], list)
        assert len(data['items']) == 4

        # Verificar ordenação por rating (maior para menor)
        ratings = [book['rating'] for book in data['items']]
        assert ratings == [5, 5, 4, 3]


def test_books_top_rated_ordered_by_rating_desc(client, mock_books_sorted_by_rating):
    """Teste: Livros devem estar ordenados por rating em ordem decrescente"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=(mock_books_sorted_by_rating, 4),
    ):
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200

        data = response.get_json()
        books = data['items']

        # Primeiro livro deve ter rating 5
        assert books[0]['rating'] == 5
        assert books[0]['title'] == "Advanced Python"

        # Segundo livro deve ter rating 5 (ordenado alfabeticamente)
        assert books[1]['rating'] == 5
        assert books[1]['title'] == "Data Science with Python"

        # Terceiro livro deve ter rating 4
        assert books[2]['rating'] == 4
        assert books[2]['title'] == "Python for Beginners"

        # Quarto livro deve ter rating 3
        assert books[3]['rating'] == 3
        assert books[3]['title'] == "A Light in the Attic"


def test_books_top_rated_no_results(client):
    """Teste: Retornar lista vazia quando não há livros"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=([], 0),
    ):
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert len(data['items']) == 0
        assert data['pagination']['total_items'] == 0
        assert data['pagination']['total_pages'] == 0


# Testes de paginação


def test_books_top_rated_with_default_pagination(client, mock_books_sorted_by_rating):
    """Teste: Paginação padrão (page=1, per_page=10)"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=(mock_books_sorted_by_rating, 4),
    ):
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200

        data = response.get_json()
        pagination = data['pagination']
        assert pagination['page'] == 1
        assert pagination['per_page'] == 10
        assert pagination['total_items'] == 4
        assert pagination['total_pages'] == 1


def test_books_top_rated_with_custom_pagination(client, mock_books_sorted_by_rating):
    """Teste: Paginação customizada"""
    first_page = mock_books_sorted_by_rating[:2]

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=(first_page, 4),
    ):
        response = client.get("/api/v1/books/top-rated?page=1&per_page=2")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) == 2
        assert data['pagination']['page'] == 1
        assert data['pagination']['per_page'] == 2
        assert data['pagination']['total_items'] == 4
        assert data['pagination']['total_pages'] == 2


def test_books_top_rated_page_2(client, mock_books_sorted_by_rating):
    """Teste: Segunda página de resultados"""
    second_page = mock_books_sorted_by_rating[2:4]

    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=(second_page, 4),
    ):
        response = client.get("/api/v1/books/top-rated?page=2&per_page=2")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) == 2
        assert data['pagination']['page'] == 2
        assert data['pagination']['per_page'] == 2


def test_books_top_rated_invalid_page_parameter(client):
    """Teste: Parâmetro page inválido (< 1)"""
    response = client.get("/api/v1/books/top-rated?page=0")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_top_rated_invalid_per_page_parameter(client):
    """Teste: Parâmetro per_page inválido (> 100)"""
    response = client.get("/api/v1/books/top-rated?per_page=101")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_top_rated_negative_page(client):
    """Teste: Parâmetro page negativo"""
    response = client.get("/api/v1/books/top-rated?page=-1")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_top_rated_zero_per_page(client):
    """Teste: Parâmetro per_page zero"""
    response = client.get("/api/v1/books/top-rated?per_page=0")
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data


def test_books_top_rated_large_page_number(client):
    """Teste: Número de página muito alto (sem resultados naquela página)"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=([], 10),
    ):
        response = client.get("/api/v1/books/top-rated?page=100&per_page=10")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data['items']) == 0
        assert data['pagination']['page'] == 100
        assert data['pagination']['total_items'] == 10


# Testes de estrutura de resposta


def test_books_top_rated_response_structure(client, mock_books_sorted_by_rating):
    """Teste: Verificar estrutura completa da resposta"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=([mock_books_sorted_by_rating[0]], 1),
    ):
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200

        data = response.get_json()

        # Verificar estrutura de alto nível
        assert 'items' in data
        assert 'pagination' in data

        # Verificar estrutura de um livro
        book = data['items'][0]
        assert 'id' in book
        assert 'title' in book
        assert 'price' in book
        assert 'rating' in book
        assert 'availability' in book
        assert 'category' in book
        assert 'image_url' in book

        # Verificar tipos
        assert isinstance(book['id'], str)
        assert isinstance(book['title'], str)
        assert isinstance(book['price'], str)
        assert isinstance(book['rating'], int)
        assert isinstance(book['availability'], str)
        assert isinstance(book['category'], str)
        assert isinstance(book['image_url'], str)

        # Verificar estrutura de paginação
        pagination = data['pagination']
        assert 'page' in pagination
        assert 'per_page' in pagination
        assert 'total_items' in pagination
        assert 'total_pages' in pagination


def test_books_top_rated_uses_items_key_for_consistency(client, mock_books_sorted_by_rating):
    """Teste: Resposta deve usar chave 'items' para consistência com outros endpoints"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=([mock_books_sorted_by_rating[0]], 1),
    ):
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200

        data = response.get_json()
        assert 'items' in data
        assert 'results' not in data


def test_books_top_rated_returns_all_book_fields(client, mock_books_sorted_by_rating):
    """Teste: Verificar que todos os campos do livro são retornados"""
    with patch(
        "app.infrastructure.repository.book_repository.BookRepository.get_top_rated_books",
        return_value=([mock_books_sorted_by_rating[0]], 1),
    ):
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200

        data = response.get_json()
        book = data['items'][0]

        # Verificar que os valores esperados estão presentes
        assert book['id'] == "550e8400-e29b-41d4-a716-446655440001"
        assert book['title'] == "Advanced Python"
        assert book['price'] == "49.99"
        assert book['rating'] == 5
        assert book['availability'] == "In stock"
        assert book['category'] == "Fiction"
        assert book['image_url'] == "https://example.com/advanced_python.jpg"
