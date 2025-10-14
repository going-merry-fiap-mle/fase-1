from flask import Blueprint, jsonify
from flask.wrappers import Response

from app.controller.categories.get_categories_controller import GetCategoriesController

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@categories_bp.route('', methods=['GET'])
def list_categories() -> Response:
    """
    Listar todas as categorias
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias
        schema:
          type: object
          properties:
            categories:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
    """
    controller = GetCategoriesController()
    categories = controller.call_controller()

    return jsonify({"categories": [category.model_dump() for category in categories]})
