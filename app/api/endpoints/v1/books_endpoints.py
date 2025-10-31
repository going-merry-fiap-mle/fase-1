from decimal import Decimal
from uuid import UUID

from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.controller.books.get_books_by_price_controller import GetBooksByPriceController
from app.controller.books.get_book_controller import GetBookController
from app.controller.books.search_books_controller import SearchBooksController
from app.controller.books.top_rated_books_controller import TopRatedBooksController
from app.schemas.pagination_schema import PaginationParams
from app.core.auth import admin_required

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")


@books_bp.route("", methods=["GET"])
@admin_required
def list_books() -> Response | tuple[Response, int]:
    """
    Listar todos os livros com paginação
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: "Número da página (mínimo: 1)"
      - name: per_page
        in: query
        type: integer
        default: 10
        description: "Itens por página (mínimo: 1, máximo: 100)"
    responses:
      200:
        description: Lista paginada de livros
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: "ID do livro (UUID)"
                  title:
                    type: string
                  price:
                    type: string
                  rating:
                    type: integer
                  availability:
                    type: string
                  category:
                    type: string
                  image_url:
                    type: string
            pagination:
              type: object
              properties:
                page:
                  type: integer
                per_page:
                  type: integer
                total_items:
                  type: integer
                total_pages:
                  type: integer
      400:
        description: Parâmetros inválidos
    """
    pagination = PaginationParams(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 10, type=int)
    )

    controller = GetBookController()
    result = controller.call_controller(page=pagination.page, per_page=pagination.per_page)

    return jsonify(result.model_dump())


@books_bp.route("/<string:book_id>", methods=["GET"])
@admin_required
def get_book(book_id: str) -> Response | tuple[Response, int]:
    """
    Buscar livro por ID
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: "ID do livro (UUID)"
    responses:
      200:
        description: Detalhes do livro
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            price:
              type: string
            rating:
              type: integer
            availability:
              type: string
            category:
              type: string
            image_url:
              type: string
      404:
        description: Livro não encontrado
      400:
        description: UUID inválido
    """
    UUID(book_id)
    return jsonify({"id": book_id, "book": None}), 200


@books_bp.route("/search", methods=["GET"])
def search_books() -> Response | tuple[Response, int]:
    """
    Buscar livros por título e/ou categoria
    ---
    tags:
      - Livros
    description: |
      Busca livros por título e/ou categoria (busca parcial, case-insensitive).

      **IMPORTANTE:** Pelo menos um parâmetro de busca (title ou category) deve ser fornecido.

      **Comportamento:**
      - Se apenas 'title' for fornecido: busca livros cujo título contenha o valor informado
      - Se apenas 'category' for fornecido: busca livros cuja categoria contenha o valor informado
      - Se ambos forem fornecidos: busca livros que satisfaçam AMBAS as condições (AND)
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: "Título do livro (busca parcial, case-insensitive). Pelo menos um parâmetro de busca é obrigatório."
      - name: category
        in: query
        type: string
        required: false
        description: "Categoria do livro (busca parcial, case-insensitive). Pelo menos um parâmetro de busca é obrigatório."
      - name: page
        in: query
        type: integer
        default: 1
        description: "Número da página (mínimo: 1)"
      - name: per_page
        in: query
        type: integer
        default: 10
        description: "Itens por página (mínimo: 1, máximo: 100)"
    responses:
      200:
        description: Lista paginada de livros encontrados
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: "ID do livro (UUID)"
                  title:
                    type: string
                  price:
                    type: string
                  rating:
                    type: integer
                  availability:
                    type: string
                  category:
                    type: string
                  image_url:
                    type: string
            pagination:
              type: object
              properties:
                page:
                  type: integer
                per_page:
                  type: integer
                total_items:
                  type: integer
                total_pages:
                  type: integer
      400:
        description: Parâmetros inválidos (ex. nenhum parâmetro de busca fornecido, paginação inválida)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid parameters"
            message:
              type: string
              example: "At least one search parameter (title or category) must be provided"
    """
    title = request.args.get('title', type=str)
    category = request.args.get('category', type=str)

    if title is not None:
        title = title.strip() or None
    if category is not None:
        category = category.strip() or None

    if not title and not category:
        return jsonify({
            "error": "Invalid parameters",
            "message": "At least one search parameter (title or category) must be provided"
        }), 400

    pagination = PaginationParams(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 10, type=int)
    )

    controller = SearchBooksController()
    result = controller.call_controller(
        title=title,
        category=category,
        page=pagination.page,
        per_page=pagination.per_page
    )

    return jsonify(result.model_dump())


@books_bp.route("/top-rated", methods=["GET"])
def get_top_rated_books() -> Response | tuple[Response, int]:
    """
    Buscar livros com maiores avaliações
    ---
    tags:
      - Livros
    description: |
      Retorna livros ordenados por rating (maior para menor).

      **Comportamento:**
      - Livros são ordenados por rating em ordem decrescente (5, 4, 3, 2, 1)
      - Em caso de empate no rating, são ordenados por título alfabeticamente
      - Suporta paginação
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: "Número da página (mínimo: 1)"
      - name: per_page
        in: query
        type: integer
        default: 10
        description: "Itens por página (mínimo: 1, máximo: 100)"
    responses:
      200:
        description: Lista paginada de livros ordenados por rating
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: "ID do livro (UUID)"
                  title:
                    type: string
                  price:
                    type: string
                  rating:
                    type: integer
                  availability:
                    type: string
                  category:
                    type: string
                  image_url:
                    type: string
            pagination:
              type: object
              properties:
                page:
                  type: integer
                per_page:
                  type: integer
                total_items:
                  type: integer
                total_pages:
                  type: integer
      400:
        description: Parâmetros de paginação inválidos
    """
    pagination = PaginationParams(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 10, type=int)
    )

    controller = TopRatedBooksController()
    result = controller.call_controller(
        page=pagination.page,
        per_page=pagination.per_page
    )

    return jsonify(result.model_dump())

@books_bp.route("/price-range", methods=["GET"])
def price_range_books() -> tuple[Response, int]:
    """
    Listar livros paginados dentro de uma faixa de preço 
    ---
    tags:
      - Livros
    parameters:
      - name: min
        in: query
        type: number
        required: true
        description: "Preço mínimo"
      - name: max
        in: query
        type: number
        required: true
        description: "Preço máximo"
      - name: page
        in: query
        type: integer
        default: 1
        description: "Número da página (mínimo: 1)"
      - name: per_page
        in: query
        type: integer
        default: 10
        description: "Itens por página (mínimo: 1, máximo: 100)"
    responses:
      200:
        description: "Lista paginada de livros"
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: "ID do livro (UUID)"
                  title:
                    type: string
                  price:
                    type: string
                  rating:
                    type: integer
                  availability:
                    type: string
                  category:
                    type: string
                  image_url:
                    type: string
            pagination:
              type: object
              properties:
                page:
                  type: integer
                per_page:
                  type: integer
                total_items:
                  type: integer
                total_pages:
                  type: integer
      400:
        description: "Parâmetros inválidos"
    """

    pagination = PaginationParams(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 10, type=int)
    )

    min_str = request.args.get('min')
    max_str = request.args.get('max')
    
    if min_str is None or max_str is None:
        return jsonify({"error": "Invalid parameters", "message": "Both min and max parameters are required"}), 400

    try:

      min_price = Decimal(min_str)
      max_price = Decimal(max_str)

    except Exception:
            return jsonify({"error": "Invalid parameters", "message": "Both min and max parameters are required"}), 400
    
    if min_price > max_price:
        return jsonify({"error": "Invalid parameters", "message": "'min' must be less than or equal to 'max'"}), 400

    controller = GetBooksByPriceController()
    result = controller.call_controller(page=pagination.page, per_page=pagination.per_page, min_price=min_price, max_price=max_price)

    
    return jsonify(result.model_dump()), 200