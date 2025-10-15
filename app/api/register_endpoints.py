from flask import Flask

from app.api.endpoints.v1.books_endpoints import books_bp
from app.api.endpoints.v1.categories_endpoints import categories_bp
from app.api.endpoints.v1.health_endpoints import health_bp
from app.api.endpoints.v1.scraper_endpoints import scraper_bp


def register_endpoints(app: Flask) -> None:
    app.register_blueprint(books_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(scraper_bp)
