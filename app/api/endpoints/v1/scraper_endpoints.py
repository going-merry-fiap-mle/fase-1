import threading

from flask import Blueprint, Response, jsonify

from app.controller.scraping_controller import ScrapingController

scraper_bp = Blueprint("scraping", __name__, url_prefix="/api/v1/scraping")


def scraping_endpoint() -> None:
    controller = ScrapingController()
    controller.call_controller()


@scraper_bp.route("", methods=["GET"])
def scraping() -> tuple[Response, int]:
    """
    Realizar o web scraping dos livros
    ---
    tags:
      - Web Scraping
    responses:
        200:
            description: Retorna a lista de livros extraídos
    """
    thread = threading.Thread(target=scraping_endpoint)
    thread.daemon = True
    thread.start()

    return jsonify("Scraping iniciado com sucesso"), 202
