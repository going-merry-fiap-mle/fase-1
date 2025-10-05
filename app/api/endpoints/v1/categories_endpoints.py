from flask import Blueprint, jsonify

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')

@categories_bp.route('', methods=['GET'])
def list_categories():
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
                type: string
    """
    return jsonify({'categories': []}), 200
