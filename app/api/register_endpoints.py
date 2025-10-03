from flask import Flask

from app.api.endpoints.v1.books import books_bp
from app.api.endpoints.v1.categories import categories_bp
from app.api.endpoints.v1.health import health_bp
from app.api.endpoints.v1.scraper import scraper_bp


def register_endpoints(app: Flask) -> None:
    app.register_blueprint(books_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(scraper_bp)
