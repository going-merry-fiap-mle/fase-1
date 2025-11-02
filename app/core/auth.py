from functools import wraps

from flask import g, jsonify, request

from app.core.security import verify_token
from app.infrastructure.models.enums.admin_enum import UserRole
from app.infrastructure.models.user import User
from app.infrastructure.session_manager import get_session


def get_current_user():
    """Get current user from JWT token"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    payload = verify_token(token)

    if not payload or payload.get("type") != "access":
        return None

    username = payload.get("sub")

    with get_session() as session:
        user = session.query(User).filter(User.username == username).first()
        if user is not None:
            session.expunge(user)
        return user


def jwt_required(f):
    """Decorator to require JWT authentication"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()

        if not user:
            return jsonify({"error": "Invalid or missing token"}), 401

        g.current_user = user
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()

        if not user:
            return jsonify({"error": "Invalid or missing token"}), 401

        if user.role != UserRole.admin:
            return jsonify({"error": "Admin access required"}), 403

        g.current_user = user
        return f(*args, **kwargs)

    return decorated_function
