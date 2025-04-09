from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.services.task_service import create_task_service, get_all_tasks_service, update_task_service, delete_task_service

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


@task_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_tasks():
    user_id = get_jwt_identity()
    tasks = get_all_tasks_service(user_id)
    return jsonify([task.to_dict() for task in tasks]), 200


@task_bp.route('/update/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task_route(task_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    title = data.get('title')
    description = data.get('description')
    status = data.get('status')

    try:
        updated_task = update_task_service(task_id, user_id, title, description, status)
        return jsonify(updated_task.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task_route(task_id):
    user_id = get_jwt_identity()
    try:
        delete_task_service(task_id, user_id)
        return jsonify({"message": "Task deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
