from flask import Flask
from api.controllers.books import books_bp
from api.controllers.categories import categories_bp
from api.controllers.health import health_bp

app = Flask(__name__)

app.register_blueprint(books_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )
