from flask import Blueprint, jsonify

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')

@categories_bp.route('', methods=['GET'])
def list_categories():
    return jsonify({'categories': []}), 200

