from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')

@health_bp.route('', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'API operacional',
        'data_connectivity': True
    }), 200
