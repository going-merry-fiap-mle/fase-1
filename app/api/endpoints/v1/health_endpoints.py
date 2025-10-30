from flask import Blueprint, jsonify
from flask.wrappers import Response

from app.controller.health.health_controller import HealthController

health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')

@health_bp.route('', methods=['GET'])
def health() -> Response | tuple[Response, int]:
    """
    Verificar status da API
    ---
    tags:
      - Saúde
    description: |
      Verifica se a API está operacional e testa a conectividade com o banco de dados.

      **Validação:**
      - Executa SELECT 1 no banco para verificar conectividade real
      - Retorna status 'ok' se tudo estiver funcionando
      - Retorna status 'error' se houver problemas de conexão
    responses:
      200:
        description: Status da API e conectividade do banco de dados
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
              description: "Status da API (ok ou error)"
            message:
              type: string
              example: "API operacional"
              description: "Mensagem descritiva do status"
            data_connectivity:
              type: boolean
              example: true
              description: "Indica se há conectividade com o banco de dados"
    """
    controller = HealthController()
    result = controller.call_controller()

    return jsonify(result.model_dump())
