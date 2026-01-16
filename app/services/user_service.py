from fastapi import status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password
from app.repositories.user_repository import create_user, get_user_by_email
from app.core.exceptions import AppException

def register_user(db: Session, user: UserCreate) -> User:
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise AppException(
            error = "EMAIL_ALREADY_EXISTS",
            message = "A user with this email already exists.",
            status_code = 409
        )
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    return create_user(db, new_user)

    