from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.jwt import ALGORITHM, SECRET_KEY
from app.schemas.auth import LoginRequest, LoginResponse, TokenResponse, RefreshTokenRequest
from app.services.auth_service import AuthService
from app.schemas.response import SucessResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from app.models.user import User
from app.schemas.error import ErrorResponse

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post(
            "/login", 
            summary = "Login with OAuth2",
            responses = {
                401: {"model": ErrorResponse, "description": "Invalid credentials"}
            })
def login_oath2(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
 
    result = AuthService.login(db, form_data.username, form_data.password)

    return {
        "access_token": result.tokens.access_token,
        "token_type": "bearer",
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
    login_response = AuthService.login(db, data.email, data.password)

    return SucessResponse(
        message = "Login successful",
        data = login_response
    )   

@router.post(
            "/refresh", 
            status_code=status.HTTP_200_OK,
            summary = "Refresh access token",
            responses = {
                401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"}
            })
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return AuthService.refresh_token(db, data.refresh_token)