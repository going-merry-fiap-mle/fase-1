from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.schemas.auth import LoginRequest, RefreshRequest
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.infrastructure.session_manager import get_session
from app.infrastructure.models.user import User

router = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@router.route('/login', methods=['POST'])
def login():
    """Login endpoint
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            token_type:
              type: string
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        login_request = LoginRequest(**data)
        
        with get_session() as session:
            user = session.query(User).filter(User.username == login_request.username).first()
            
            if not user or not verify_password(login_request.password, user.password):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            access_token = create_access_token(data={"sub": user.username})
            refresh_token = create_refresh_token(data={"sub": user.username})
            
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer'
            })
            
    except ValidationError as e:
        return jsonify({'error': 'Invalid request data', 'details': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@router.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh token endpoint
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - refresh_token
          properties:
            refresh_token:
              type: string
    responses:
      200:
        description: Token refreshed successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            token_type:
              type: string
      401:
        description: Invalid refresh token
    """
    try:
        data = request.get_json()
        refresh_request = RefreshRequest(**data)
        
        payload = verify_token(refresh_request.refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            return jsonify({'error': 'Invalid refresh token'}), 401
        
        username = payload.get("sub")
        
        with get_session() as session:
            user = session.query(User).filter(User.username == username).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            access_token = create_access_token(data={"sub": user.username})
            new_refresh_token = create_refresh_token(data={"sub": user.username})
            
            return jsonify({
                'access_token': access_token,
                'refresh_token': new_refresh_token,
                'token_type': 'bearer'
            })
            
    except ValidationError as e:
        return jsonify({'error': 'Invalid request data', 'details': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500