from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.controller.categories.get_categories_controller import GetCategoriesController
from app.schemas.pagination_schema import PaginationParams

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@categories_bp.route('', methods=['GET'])
def list_categories() -> Response | tuple[Response, int]:
    """
    Listar todas as categorias com paginação
    ---
    tags:
      - Categorias
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
        description: Lista paginada de categorias
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
                    description: "ID da categoria (UUID)"
                  name:
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

    controller = GetCategoriesController()
    result = controller.call_controller(page=pagination.page, per_page=pagination.per_page)

    return jsonify(result.model_dump())
