from flask import Flask
from flasgger import Swagger
from api.controllers.books import books_bp
from api.controllers.categories import categories_bp
from api.controllers.health import health_bp

app = Flask(__name__)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Livros FIAP",
        "description": "Projeto da Fase 1 da Pós em Machine Learning Engineering - Equipe Going Merry",
        "version": "1.0.0",
        "license": {
            "name": "MIT"
        }
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ]
}
swagger = Swagger(app, template=swagger_template)

app.register_blueprint(books_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )
