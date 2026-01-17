from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_cnpj(db: Session, cnpj: str) -> User:
    return db.query(User).filter(User.cnpj == cnpj).first()

def get_user_by_cnh(db: Session, cnh_number: str) -> User:
    return db.query(User).filter(User.cnh_number == cnh_number).first()

