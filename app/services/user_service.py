from datetime import timedelta
import re
from app.models.user import User
from app import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

class UserAlreadyExists(Exception):
    pass

class PasswordTooShort(Exception):
    pass

class InvalidEmailFormat(Exception):
    pass

class InvalidCredentials(Exception):
    pass


def create_user(username, email, password):
    """
    Creates a new user with the provided username, email, and password.
    Raises exceptions for validation and uniqueness issues.
    """

    if not re.match(EMAIL_REGEX, email):
        raise InvalidEmailFormat("Invalid email format")

    if len(password) < 6:
        raise PasswordTooShort("Password must be at least 6 characters long")

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        raise UserAlreadyExists("Username or email already exists")

    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    except IntegrityError:
        db.session.rollback()
        raise UserAlreadyExists("Username or email already exists (db error)")

    except Exception as e:
        db.session.rollback()
        raise Exception(f"Unexpected error: {str(e)}")

def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        raise InvalidCredentials("Invalid email or password")

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
    return access_token