from app.database import SessionLocal
from app.services.user_service import UserService

def create_default_admin():
    db = SessionLocal()

    try:
        UserService.create_admin_if_not_exists(db)
    finally:
        db.close()