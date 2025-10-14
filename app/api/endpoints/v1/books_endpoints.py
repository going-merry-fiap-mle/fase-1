from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.controller.books.get_book_controller import GetBookController
from app.controller.books.search_books_controller import SearchBooksController

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")


@books_bp.route("", methods=["GET"])
def list_books() -> Response:
    """
    Listar todos os livros
    ---
    tags:
      - Livros
    responses:
      200:
        description: Lista de livros
        schema:
          type: object
          properties:
            books:
              type: array
              items:
                type: object
    """
    controller = GetBookController()
    books = controller.call_controller()

    return jsonify({"books": [books_item.model_dump() for books_item in books]})


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """
    Buscar livro por ID
    ---
    tags:
      - Livros
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID do livro
    responses:
      200:
        description: Detalhes do livro
        schema:
          type: object
          properties:
            id:
              type: integer
            book:
              type: object
    """
    return jsonify({"id": book_id, "book": None}), 200


@books_bp.route("/search", methods=["GET"])
def search_books() -> Response:
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
    title = request.args.get("title")
    category = request.args.get("category")

    controller = SearchBooksController()
    books = controller.call_controller(title=title, category=category)

    return jsonify({"results": [book.model_dump() for book in books]})
