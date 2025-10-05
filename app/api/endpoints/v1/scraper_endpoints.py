from flask import Blueprint, Response, jsonify

from app.controller.scraping_controller import ScrapingController
from app.schemas.scraping_schema import ScrapingBase

scraper_bp = Blueprint("scraping", __name__, url_prefix="/api/v1/scraping")


@scraper_bp.route("", methods=["GET"])
def scraping() -> list[ScrapingBase] | Response:
    """
    Realizar o web scraping dos livros
    ---
    tags:
      - Web Scraping
    responses:
        200:
            description: Retorna a lista de livros extraídos
    """
    controller = ScrapingController()
    scraping = controller.call_controller()

    return jsonify([scraping_item.model_dump() for scraping_item in scraping])
