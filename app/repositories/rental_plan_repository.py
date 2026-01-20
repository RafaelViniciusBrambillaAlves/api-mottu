from sqlalchemy.orm import Session
from app.models.rental_plan import RentalPlan

class RentalPlanRepository:

    @staticmethod
    def get_by_days(db: Session, days: int) -> RentalPlan:
        return db.query(RentalPlan).filter(RentalPlan.days == days).first()
    
    @staticmethod
    def list_all(db: Session) -> list[RentalPlan]:
        return db.query(RentalPlan).all()
