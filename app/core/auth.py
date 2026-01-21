from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.jwt import decode_token
from app.api.deps import get_db
from app.models.user import User
from app.core.jwt import SECRET_KEY, ALGORITHM
from app.core.exceptions import AppException
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:

    try:
        payload = decode_token(token)
    except JWTError:
        raise AppException(
            error = "INVALID_TOKEN",
            message = "Invalid or expired token.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    if payload.get("type") != "access":
        raise AppException(
            error = "INVALID_TOKEN_TYPE",
            message = "Access token required.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    
    user_id = payload.get("sub")

    if not user_id:
        raise AppException(
            error="INVALID_TOKEN2",
            message="Invalid token payload.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user = UserRepository.get_by_id(db, int(user_id))

    if not user:
        raise AppException(
            error = "USER_NOT_FOUND",
            message = "User not found.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    return user
    
def require_access_token(token_data: dict): 
    if token_data.get("type") != "access":
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token type"
        )


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise AppException(
            error = "FORBIDDEN", 
            message = "Admin access required.",
            status_code = status.HTTP_403_FORBIDDEN
        )

    return user