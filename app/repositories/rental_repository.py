from sqlalchemy.orm import Session
from app.models.rental import Rental

def create_rental(db: Session, rental: Rental):
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental

