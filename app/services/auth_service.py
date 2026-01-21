from sqlalchemy.orm import Session 
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.exceptions import AppException
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse, LoginResponse

class AuthService:

    @staticmethod
    def login(db: Session, email: str, password: str) -> LoginResponse:
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.password):
            raise AppException(
                error = "INVALID_CREDENTIALS",
                message = "Email or password is incorrect.",
                status_code = status.HTTP_401_UNAUTHORIZED

            )
        
        tokens = TokenResponse(
            access_token = create_access_token(user.id, user.role),
            refresh_token = create_refresh_token(user.id)
        )

        return LoginResponse(user = user, tokens = tokens)
    
    @staticmethod
    def refresh_token(db: Session, refresh_token: str):
        try:
            payload = decode_token(refresh_token)
        
        except:
            raise AppException(
                error = "INVALID_TOKEN", 
                message = "Invalid refresh token",
                status_code = status.HTTP_401_UNAUTHORIZED
            )

        if payload.get("type") != "refresh":
            raise AppException(
                error = "INVALID_TOKEN_TYPE", 
                message = "User not found.", 
                status_code = status.HTTP_401_UNAUTHORIZED
            )
        
        user = UserRepository.get_by_id(db, int(payload.get("sub")))

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND", 
                message = "User not found", 
                status_code = status.HTTP_401_UNAUTHORIZED 
            )
        
        return TokenResponse(
            access_token = create_access_token(user.id, user.role),
            refresh_token = refresh_token
        )
    