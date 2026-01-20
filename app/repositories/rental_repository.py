from sqlalchemy.orm import Session
from app.models.rental import Rental
from typing import Optional

class RentalRepository:

    @staticmethod
    def create(db: Session, rental: Rental) -> Rental:
        db.add(rental)
        db.commit()
        db.refresh(rental)
        return rental

    @staticmethod
    def get_by_id(db: Session, rental_id: int) -> Optional[Rental]:
        return db.query(Rental).filter(Rental.id == rental_id).first()

    @staticmethod
    def list_all(db: Session) -> list[Rental]:
        return db.query(Rental).all()
    
    @staticmethod
    def list_by_motorcycle(db: Session, motorcycle_id: int) -> list[Rental]:
        return db.query(Rental).filter(Rental.motorcycle_id == motorcycle_id).all()
    
    @staticmethod
    def list_by_user(db: Session, user_id: int) -> list[Rental]:
        return db.query(Rental).filter(Rental.user_id == user_id).all()

    @staticmethod
    def has_active_rental(db: Session, motorcycle_id: int) -> Optional[Rental]:
        return db.query(Rental).filter(Rental.motorcycle_id == motorcycle_id, Rental.status == "active").first()

    @staticmethod
    def finished(db: Session, rental: Rental) -> Rental:
        db.add(rental)
        db.commit()
        db.refresh(rental)
        return rental