from flask import Blueprint, jsonify
from typing import Tuple
from flask.wrappers import Response

from app.infrastructure.adapters.book_adapter import BookAdapter
from app.services.book_service import BookService

health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')

@health_bp.route('', methods=['GET'])
def health() -> Tuple[Response, int]:
    """
    Verificar status da API e conectividade com os dados
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
    # Tenta verificar conectividade real com os dados
    data_connectivity = False
    try:
        book_adapter = BookAdapter()
        book_service = BookService(book_adapter)
        books = book_service.get_books()
        # Se conseguiu acessar sem exceção, conectividade OK
        data_connectivity = True
    except Exception:
        data_connectivity = False

    status = 'ok' if data_connectivity else 'degraded'
    message = 'API operacional' if data_connectivity else 'API operacional, mas sem conectividade com dados'

    return jsonify({
        'status': status,
        'message': message,
        'data_connectivity': data_connectivity
    }), 200
