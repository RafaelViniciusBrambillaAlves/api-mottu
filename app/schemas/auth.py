from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserPublic

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length = 6, max_length = 72)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class LoginResponse(BaseModel):
    user: UserPublic
    tokens: TokenResponse
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str