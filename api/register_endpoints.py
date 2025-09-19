"""
Função para registrar todos os blueprints/endpoints da API Flask.
"""
from api.controllers.books import books_bp
from api.controllers.categories import categories_bp
from api.controllers.health import health_bp

def register_endpoints(app):
    """
    Registra todos os blueprints/endpoints na aplicação Flask.
    Args:
        app (Flask): Instância da aplicação Flask.
    """
    app.register_blueprint(books_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(health_bp)

