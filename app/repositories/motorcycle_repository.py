from sqlalchemy.orm import Session
from app.models.motorcycle import Motorcycle
from sqlalchemy import exists
from app.models.rental import Rental
from typing import Optional

def create_motorcycle(db: Session, motorcycle: Motorcycle) -> Motorcycle:
    db.add(motorcycle)
    db.commit()
    db.refresh(motorcycle)
    return motorcycle

def get_motorcycle_by_vin(db: Session, vin: str) -> Motorcycle:
    return db.query(Motorcycle).filter(Motorcycle.vin == vin).first()

def update_motorcycle(db: Session, motorcycle: Motorcycle, new_vin: str) -> Motorcycle:
    motorcycle.vin = new_vin
    db.commit()
    db.refresh(motorcycle)
    return motorcycle

def get_available_motorcycle(db: Session) -> list[Motorcycle]:
    return db.query(Motorcycle).filter(~exists().where(
                                                        (Rental.motorcycle_id == Motorcycle.id) &
                                                        (Rental.status == "active")
                                                    )).all()

def get_motorcycle_by_id(db: Session, motorcycle_id: int) -> Optional[Motorcycle]: 
    return db.query(Motorcycle).filter(Motorcycle.id == motorcycle_id).first()

def delete_motorcycle(db: Session, motorcycle: Motorcycle) -> None:
    db.delete(motorcycle)
    db.commit()

    