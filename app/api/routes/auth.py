from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.jwt import ALGORITHM, SECRET_KEY
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import login_user, create_access_token
from app.schemas.response import SucessResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from app.models.user import User

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post("/login", status_code = status.HTTP_200_OK)
def login_oath2(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
 
    user, tokens = login_user(db, form_data.username, form_data.password)

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer"
    }

@router.post("/login/json", status_code = status.HTTP_200_OK, response_model = SucessResponse[LoginResponse])
def login_json(data: LoginRequest, db: Session = Depends(get_db)):
    user, tokens = login_user(db, data.email, data.password)

    return SucessResponse(
        message = "Login successful",
        data = LoginResponse(
            user= user,
            tokens = tokens
        )
    )   

@router.post("/refresh")
def refresh_token(token: str, db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token type")(
        )
    
    user_id: int = payload.get("sub")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "User not found"
        )

    return {
        "acces_token": create_access_token(user.id, user.role),
        "token_type": "bearer"
    }