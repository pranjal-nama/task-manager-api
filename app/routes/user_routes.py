from flask import request, jsonify, Blueprint
from app.services.user_service import create_user, login_user, UserAlreadyExists, PasswordTooShort, InvalidEmailFormat, InvalidCredentials

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if username:
        username = username.strip()
    if email:
        email = email.strip()

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    try:
        user = create_user(username, email, password)
        return jsonify({"message": "User created successfully", "user_id": user.id}), 201

    except InvalidEmailFormat as e:
        return jsonify({"error": str(e)}), 400

    except UserAlreadyExists as e:
        return jsonify({"error": str(e)}), 400

    except PasswordTooShort as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email:
            email = email.strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        access_token = login_user(email, password)
        return jsonify({"access_token": access_token}), 200
    except InvalidCredentials as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500