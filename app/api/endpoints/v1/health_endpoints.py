from flask import Blueprint, jsonify
from typing import Tuple
from flask.wrappers import Response

health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')

@health_bp.route('', methods=['GET'])
def health() -> Tuple[Response, int]:
    """
    Verificar status da API
    ---
    tags:
      - Saúde
    responses:
      200:
        description: Status da API
        schema:
          type: object
          properties:
            status:
              type: string
            message:
              type: string
            data_connectivity:
              type: boolean
    """
    return jsonify({
        'status': 'ok',
        'message': 'API operacional',
        'data_connectivity': True
    }), 200
