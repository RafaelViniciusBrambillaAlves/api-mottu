from sqlalchemy.orm import Session
from app.models.motorcycle import Motorcycle

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

