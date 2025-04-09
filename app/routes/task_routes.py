from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.task_service import create_task_service

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/create', methods=['POST'])
@jwt_required()
def create_task_route():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'pending')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    user_id = get_jwt_identity()
    try:
        task = create_task_service(user_id=user_id, title=title, description=description, status=status)
        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
