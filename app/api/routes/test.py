from fastapi import APIRouter, Depends
from app.core.auth import get_current_user, require_admin
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

@router.get("/admin")
def admin_route(current_user: User = Depends(require_admin)):
    return {
        "message": "This is an admin-only route. Admin authentication successful.",
        "user_id": current_user.id,
        "email": current_user.email
    }