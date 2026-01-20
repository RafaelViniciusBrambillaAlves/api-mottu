from fastapi import APIRouter, Depends, status 
from sqlalchemy.orm import Session
from app.schemas.user import AdminCreate, UserResponse
from app.schemas.response import SucessResponse
from app.services.user_service import UserService
from app.api.deps import get_db
from app.core.auth import require_admin
from app.models.user import User
from app.schemas.error import ErrorResponse

router = APIRouter(prefix = "/admin", tags = ["admin"])

@router.post(
            "/users", 
            status_code = status.HTTP_201_CREATED, 
            response_model = SucessResponse[UserResponse],
            summary = "Create admin user",
            responses = {
                401: {"model": ErrorResponse, "description": "Unauthorized"},
                403: {"model": ErrorResponse, "description": "Admin access required"},
                409: {"model": ErrorResponse, "description": "Email already exists"},
            })
def create_admin(admin: AdminCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    
    new_admin = UserService.register_admin(db, admin)

    return SucessResponse(
        message = "Admin user created successfully.",
        data = UserResponse.model_validate(new_admin, from_attributes = True)
    )

