from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:

    @staticmethod
    def create(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_cnpj(db: Session, cnpj: str) -> User:
        return db.query(User).filter(User.cnpj == cnpj).first()

    @staticmethod
    def get_by_cnh(db: Session, cnh_number: str) -> User:
        return db.query(User).filter(User.cnh_number == cnh_number).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
