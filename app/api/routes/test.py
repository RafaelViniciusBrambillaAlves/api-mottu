from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix = "/test", tags = ["test"])

@router.get("/public")
def public_route():
    return {
        "message": "This is a public route. No authentication required."
    }

@router.get("/private")
def private_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "This is  protected route. Authentication successful.",
        "user_id": current_user.id,
        "email": current_user.email
    }   