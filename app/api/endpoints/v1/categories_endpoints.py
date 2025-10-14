from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.controller.categories.get_categories_controller import GetCategoriesController

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@categories_bp.route('', methods=['GET'])
def list_categories() -> Response:
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
        description: Número da página
      - name: per_page
        in: query
        type: integer
        default: 10
        description: Itens por página
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
                    description: ID da categoria (UUID)
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
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:
            per_page = 100

        controller = GetCategoriesController()
        result = controller.call_controller(page=page, per_page=per_page)

        return jsonify(result.model_dump())
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
