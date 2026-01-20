from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.jwt import ALGORITHM, SECRET_KEY
from app.schemas.auth import LoginRequest, LoginResponse, TokenResponse
from app.services.auth_service import AuthService
from app.schemas.response import SucessResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from app.models.user import User
from app.schemas.error import ErrorResponse

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post(
            "/login", 
            status_code = status.HTTP_200_OK,
            summary = "Login with OAuth2",
            responses = {
                401: {"model": ErrorResponse, "description": "Invalid credentials"}
            })
def login_oath2(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
 
    _, tokens = AuthService.login(db, form_data.username, form_data.password)

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer"
    }

@router.post(
            "/login/json", 
            response_model = SucessResponse[LoginResponse],
            summary = "Login using JSON payload",
            responses = {
                401: {"model": ErrorResponse, "description": "Invalid credentials"},
                404: {"model": ErrorResponse, "description": "User not found"},
            })
def login_json(data: LoginRequest, db: Session = Depends(get_db)):
    user, tokens =AuthService.login(db, data.email, data.password)

    return SucessResponse(
        message = "Login successful",
        data = LoginResponse(
            user= user,
            tokens = TokenResponse(**tokens)
        )
    )   

@router.post(
            "/refresh", 
            status_code=status.HTTP_200_OK,
            summary = "Refresh access token",
            responses = {
                401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"}
            })
def refresh_token(token: str, db: Session = Depends(get_db)):
    return AuthService.refresh_token(db, token)