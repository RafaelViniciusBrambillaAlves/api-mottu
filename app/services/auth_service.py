from sqlalchemy.orm import Session 
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.core.exceptions import AppException

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Email or password is incorrect",
        )
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return user, tokens