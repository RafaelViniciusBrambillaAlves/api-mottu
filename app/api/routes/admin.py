from fastapi import APIRouter, Depends, status 
from sqlalchemy.orm import Session
from app.schemas.user import AdminCreate, UserResponse
from app.schemas.response import SucessResponse
from app.services.user_service import register_admin
from app.api.deps import get_db
from app.core.auth import require_admin
from app.models.user import User

router = APIRouter(prefix = "/admin", tags = ["admin"])

@router.post("/users", status_code = status.HTTP_201_CREATED, response_model = SucessResponse[UserResponse])
def create_admin(admin: AdminCreate, db: Session = Depends(get_db), current_admin: User = Depends(require_admin)):
    
    admin = register_admin(db, admin)

    return SucessResponse(
        message = "Admin user created successfully.",
        data = UserResponse.model_validate(admin, from_attributes = True)
    )

