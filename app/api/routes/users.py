from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import SucessResponse
from app.services.user_service import register_user
from app.api.deps import get_db

router = APIRouter(prefix = "/users", tags = ["users"])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = SucessResponse[UserResponse])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = register_user(db, user)

    return SucessResponse(
        message = "User created successfully.",
        data = UserResponse.model_validate(created_user, from_attributes = True)
    )

