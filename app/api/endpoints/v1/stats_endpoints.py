from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.controller.categories.get_category_stats_controller import GetCategoryStatsController
from app.schemas.pagination_schema import PaginationParams
from app.controller.stats.get_overview_stats_controller import GetOverviewStatsController

stats_bp = Blueprint('stats', __name__, url_prefix='/api/v1/stats')


@stats_bp.route('/categories', methods=['GET'])
def categories_stats() -> Response | tuple[Response, int]:
    """
    Estatísticas detalhadas por categoria (quantidade de livros, preços por categoria)
    ---
    tags:
      - Estatísticas
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
        description: Lista de estatísticas por categoria (paginada)
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    description: "Nome da categoria"
                  book_count:
                    type: integer
                    description: "Quantidade de livros na categoria"
                  min_price:
                    type: number
                    format: float
                    description: "Menor preço (nullable)"
                  max_price:
                    type: number
                    format: float
                    description: "Maior preço (nullable)"
                  avg_price:
                    type: number
                    format: float
                    description: "Preço médio (nullable)"
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
    """
    pagination = PaginationParams(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 10, type=int)
    )

    controller = GetCategoryStatsController()
    result = controller.call_controller(page=pagination.page, per_page=pagination.per_page)

    return jsonify(result.model_dump())


@stats_bp.route('/overview', methods=['GET'])
def overview_stats() -> Response | tuple[Response, int]:
    """
    Estatísticas gerais (total de livros, preço médio, distribuição de ratings)
    ---
    tags:
      - Estatísticas
    responses:
      200:
        description: Overview statistics
        schema:
          type: object
          properties:
            total_books:
              type: integer
            avg_price:
              type: number
              format: float
              nullable: true
            rating_distribution:
              type: object
              additionalProperties:
                type: integer
    """
    controller = GetOverviewStatsController()
    result = controller.call_controller()

    return jsonify(result.model_dump())
