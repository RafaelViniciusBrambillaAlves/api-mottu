from fastapi import status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, AdminCreate
from app.models.user import User
from app.core.security import hash_password
from app.repositories.user_repository import create_user, get_user_by_email, get_user_by_cnpj, get_user_by_cnh, get_user_by_id
from app.core.exceptions import AppException

def _validate_email(db: Session, email: str):
    if get_user_by_email(db, email):
        raise AppException(
            error = "EMAIL_ALREADY_EXISTS",
            message = "A user with this email already exists.",
            status_code = status.HTTP_409_CONFLICT
        )

def _validate_cnpj(db: Session, cnpj: str):
    if get_user_by_cnpj(db, cnpj):
        raise AppException(
            error = "EMAIL_ALREADY_EXISTS",
            message = "A user with this CNPJ already exists.",
            status_code = status.HTTP_409_CONFLICT
        )

def _validate_cnh(db: Session, cnh_number: str):
    if get_user_by_cnh(db, cnh_number):
        raise AppException(
            error = "EMAIL_ALREADY_EXISTS",
            message = "A user with this CNH number already exists.",
            status_code = status.HTTP_409_CONFLICT
        )

def _validate_cnh_type(cnh_type: str):
    valid_types = ['A', 'B', 'AB']
    if cnh_type not in valid_types:
        raise AppException(
            error = "INVALID_CNH_TYPE",
            message = f"CNH type must be one of the following: {', '.join(valid_types)}.",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    
def register_user(db: Session, user: UserCreate) -> User:

    _validate_email(db, user.email)
    _validate_cnpj(db, user.cnpj)
    _validate_cnh(db, user.cnh_number)
    _validate_cnh_type(user.cnh_type)

    new_user = User(
        name = user.name,
        email = user.email,
        password = hash_password(user.password), 
        role = "user", 
        cnpj = user.cnpj,
        birthday = user.birthday,
        cnh_number = user.cnh_number,
        cnh_type = user.cnh_type
    )

    return create_user(db, new_user)

def register_admin(db: Session, user: AdminCreate) -> User:

    _validate_email(db, user.email)

    new_admin = User(
        name = user.name,
        email = user.email,
        password = hash_password(user.password),
        role = "admin"
    )

    return create_user(db, new_admin)