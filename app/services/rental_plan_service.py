from fastapi import status 
from sqlalchemy.orm import Session
from app.core.exceptions import AppException
from app.repositories.rental_plan_repository import RentalPlanRepository
from app.models.rental_plan import RentalPlan

class RentalPlanService:

    @staticmethod
    def get_by_days(db: Session, days: int) -> RentalPlan:
        plan = RentalPlanRepository.get_by_days(db, days)

        if not plan:
            raise AppException(
                error = "RENTAL_PLAN_NOT_FOUND",
                message = "Rental plan not found",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return plan