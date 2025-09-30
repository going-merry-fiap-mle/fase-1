import os
from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
from api.register_endpoints import register_endpoints

load_dotenv()
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

register_endpoints(app)

if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)
