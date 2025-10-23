from decimal import Decimal
from uuid import UUID

from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.controller.books.get_books_by_price_controller import GetBooksByPriceController
from app.controller.books.get_book_controller import GetBookController
from app.schemas.pagination_schema import PaginationParams

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")


@books_bp.route("", methods=["GET"])
def list_books() -> Response | tuple[Response, int]:
    """
    Listar todos os livros com paginação
    ---
    tags:
      - Livros
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
def get_book(book_id: str) -> Response | tuple[Response, int]:
    """
    Buscar livro por ID
    ---
    tags:
      - Livros
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
def search_books() -> tuple[Response, int]:
    """
    Buscar livros por título e/ou categoria
    ---
    tags:
      - Livros
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: Título do livro
      - name: category
        in: query
        type: string
        required: false
        description: Categoria do livro
    responses:
      200:
        description: Resultados da busca
        schema:
          type: object
          properties:
            results:
              type: array
              items:
                type: object
    """
    return jsonify({"results": []}), 200


@books_bp.route("/price-range", methods=["GET"])
def price_range_books() -> tuple[Response, int]:
    """
    List paginated books within price range 
    ---
    tags:
      - Livros
    parameters:
      - name: min
        in: query
        type: number
        required: true
        description: Minimum price
      - name: max
        in: query
        type: number
        required: true
        description: Maximum price
      - name: page
        in: query
        type: integer
        default: 1
        description: "Page number (min: 1)"
      - name: per_page
        in: query
        type: integer
        default: 10
        description: "Itens per page (min: 1, max: 100)"
    responses:
      200:
        description: Paginated item list
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
                    description: "Book ID (UUID)"
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
        description: Invalid parameters
    """

    pagination = PaginationParams(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 10, type=int)
    )

    min_str = request.args.get('min')
    max_str = request.args.get('max')
    
    if min_str is None or max_str is None:
        return jsonify({"description": "Invalid parameters"}), 400

    try:

      min_price = Decimal(min_str)
      max_price = Decimal(max_str)

    except ValueError:
            return jsonify({"description": "Invalid parameters"}), 400

    controller = GetBooksByPriceController()
    result = controller.call_controller(page=pagination.page, per_page=pagination.per_page, min_price=min_price, max_price=max_price)

    
    return jsonify({"results": result.model_dump()}), 200