from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import SucessResponse
from app.services.user_service import UserService
from app.services.cnh_photo_service import CNHPhotoService
from app.api.deps import get_db
from app.schemas.error import ErrorResponse
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.auth import get_current_user

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

@router.post(
            "/me/cnh-photo",
            status_code = status.HTTP_201_CREATED, 
            response_model = SucessResponse[UserResponse],
            responses={
                401: {"model": ErrorResponse},
                406: {"model": ErrorResponse},
                500: {"model": ErrorResponse},
            })
def upload_cnh_photo(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    update_user = UserService.upload_cnh_photo(
        db = db, 
        user = current_user,
        file = file
    ) 

    return SucessResponse(
        message = "CNH photo uploaded successfully.",
        data = UserResponse.model_validate(update_user)
    )