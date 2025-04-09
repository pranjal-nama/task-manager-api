from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    default_db_path = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', default_db_path)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.models.user import User
    from app.models.task import Task

    with app.app_context():
        db.create_all()

    from app.routes.user_routes import auth_bp
    # from app.routes import task_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(task_bp, url_prefix="/api/tasks")

    return app
