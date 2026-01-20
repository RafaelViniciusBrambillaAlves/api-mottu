from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import SucessResponse
from app.services.user_service import UserService
from app.api.deps import get_db
from app.schemas.error import ErrorResponse

router = APIRouter(prefix = "/users", tags = ["users"])

@router.post(
        "/", 
        status_code = status.HTTP_201_CREATED, 
        response_model = SucessResponse[UserResponse],
        responses = {
            400: {"model": ErrorResponse, "description": "Invalid data"}, 
            409: {"model": ErrorResponse, "description": "User already exists"},
            500: {"model": ErrorResponse, "description": "Internal server error"}
        })
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = UserService.register_user(db, user)

    return SucessResponse(
        message = "User created successfully.",
        data = UserResponse.model_validate(created_user, from_attributes = True)
    )

