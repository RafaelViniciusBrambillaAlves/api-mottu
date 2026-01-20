from sqlalchemy.orm import Session
from app.models.motorcycle import Motorcycle
from sqlalchemy import exists
from app.models.rental import Rental
from typing import Optional, List

class MotorcycleRepository:

    @staticmethod
    def create(db: Session, motorcycle: Motorcycle) -> Motorcycle:
        db.add(motorcycle)
        db.commit()
        db.refresh(motorcycle)
        return motorcycle
    
    @staticmethod
    def get_by_id(db: Session, motorcycle_id: int) -> Optional[Motorcycle]: 
        return db.query(Motorcycle).filter(Motorcycle.id == motorcycle_id).first()
    
    @staticmethod
    def get_by_vin(db: Session, vin: str) -> Motorcycle:
        return db.query(Motorcycle).filter(Motorcycle.vin == vin).first()
    
    @staticmethod
    def list_all(db: Session) -> List[Motorcycle]:
        return db.query(Motorcycle).all()

    @staticmethod
    def list_available(db: Session) -> List[Motorcycle]:
        return db.query(Motorcycle).filter(
                                            ~exists().where(
                                                            (Rental.motorcycle_id == Motorcycle.id) &
                                                            (Rental.status == "active")
                                                            )
                                            ).all()

    @staticmethod
    def update_vin(db: Session, motorcycle: Motorcycle, vin: str) -> Motorcycle:
        motorcycle.vin = vin
        db.commit()
        db.refresh(motorcycle)
        return motorcycle

    @staticmethod
    def delete(db: Session, motorcycle: Motorcycle) -> None:
        db.delete(motorcycle)
        db.commit()

    @staticmethod
    def has_rentals(db: Session, motorcylce_id: int) -> bool:
        return db.query(exists().where(Rental.motorcycle_id == motorcylce_id)).scalar()

        