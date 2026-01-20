from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.models.rental_plan import RentalPlan
from typing import Optional

def create_rental(db: Session, rental: Rental):
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental

def get_rental_by_id(db: Session, rental_id: int) -> Optional[Rental]:
    return db.query(Rental).filter(Rental.id == rental_id).first()

def get_plan_by_days(db: Session, plan_days: int):
    return db.query(RentalPlan).filter(RentalPlan.days == plan_days).first()

def finished_rental(db: Session, rental: Rental) -> Rental:
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental