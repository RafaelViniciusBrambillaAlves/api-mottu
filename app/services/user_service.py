from fastapi import status, UploadFile
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, AdminCreate
from app.models.user import User
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.core.exceptions import AppException
from app.services.cnh_photo_service import CNHPhotoService

VALID_CNH_TYPES = {"A", "B", "AB"}
class UserService:

    @staticmethod
    def _validate_email(db: Session, email: str):
        if UserRepository.get_by_email(db, email):
            raise AppException(
                error = "EMAIL_ALREADY_EXISTS",
                message = "A user with this email already exists.",
                status_code = status.HTTP_409_CONFLICT
            )

    @staticmethod
    def _validate_cnpj(db: Session, cnpj: str):
        if UserRepository.get_by_cnpj(db, cnpj):
            raise AppException(
                error = "EMAIL_ALREADY_EXISTS",
                message = "A user with this CNPJ already exists.",
                status_code = status.HTTP_409_CONFLICT
            )

    @staticmethod
    def _validate_cnh(db: Session, cnh_number: str):
        if UserRepository.get_by_cnh(db, cnh_number):
            raise AppException(
                error = "EMAIL_ALREADY_EXISTS",
                message = "A user with this CNH number already exists.",
                status_code = status.HTTP_409_CONFLICT
            )

    @staticmethod
    def _validate_cnh_type(cnh_type: str):
        if cnh_type and cnh_type not in VALID_CNH_TYPES:
            raise AppException(
                error = "INVALID_CNH_TYPE",
                message="CNH type must be A, B or AB.",
                status_code = status.HTTP_400_BAD_REQUEST
            )

    @classmethod   
    def register_user(cls, db: Session, user: UserCreate) -> User:

        cls._validate_email(db, user.email)
        cls._validate_cnpj(db, user.cnpj)
        cls._validate_cnh(db, user.cnh_number)
        cls._validate_cnh_type(user.cnh_type)

        new_user = User(
            name = user.name,
            email = user.email,
            password = hash_password(user.password), 
            role = "user", 
            cnpj = user.cnpj,
            birthday = user.birthday,
            cnh_number = user.cnh_number,
            cnh_type = user.cnh_type
        )

        return UserRepository.create(db, new_user)

    @classmethod
    def register_admin(cls, db: Session, user: AdminCreate) -> User:

        cls._validate_email(db, user.email)

        new_admin = User(
            name = user.name,
            email = user.email,
            password = hash_password(user.password),
            role = "admin"
        )

        return UserRepository.create(db, new_admin)
    
    @staticmethod
    def upload_cnh_photo(db: Session, user: User, file: UploadFile) -> User:
        photo_path = CNHPhotoService.upload(user_id = user.id, file = file)

        return UserRepository.update_cnh_photo(db, user, photo_path)
    
    @staticmethod
    def create_admin_if_not_exists(db: Session) -> None:
        admin_email  = "admin@example.com"

        admin = UserRepository.get_by_email(db, admin_email)
        if admin:
            return 
        
        admin_user = User(
            email = admin_email,
            password = hash_password("123456"),
            role = "ADMIN"
        )

        UserRepository.create(db, admin_user)

        