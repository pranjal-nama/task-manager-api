from app import db
from app.models.task import Task

VALID_STATUSES = {"pending", "in-progress", "completed"}

def create_task_service(user_id, title, description=None, status="pending"):
    if status not in VALID_STATUSES:
        raise ValueError("Invalid status. Must be 'pending', 'in-progress', or 'completed'.")

    task = Task(
        title=title,
        description=description,
        status=status,
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    return task


def get_all_tasks_service(user_id):
    return Task.query.filter_by(user_id=user_id).order_by(Task.created_time.desc()).all()


def update_task_service(task_id, user_id, title=None, description=None, status=None):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        raise ValueError("Task not found")

    if status and status not in VALID_STATUSES:
        raise ValueError("Invalid status. Must be 'pending', 'in-progress', or 'completed'.")

    if title:
        task.title = title
    if description:
        task.description = description
    if status:
        task.status = status

    db.session.commit()
    return task


def delete_task_service(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        raise ValueError("Task not found or not authorized to delete")
    
    db.session.delete(task)
    db.session.commit()
