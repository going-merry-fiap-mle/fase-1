from flask import Blueprint, jsonify

books_bp = Blueprint('books', __name__, url_prefix='/api/v1/books')

@books_bp.route('', methods=['GET'])
def list_books():
    return jsonify({'books': []}), 200

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    return jsonify({'id': book_id, 'book': None}), 200

@books_bp.route('/search', methods=['GET'])
def search_books():
    return jsonify({'results': []}), 200
