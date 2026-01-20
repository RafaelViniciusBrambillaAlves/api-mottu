from sqlalchemy.orm import Session
from fastapi import status
from app.core.exceptions import AppException
from app.models.rental import Rental 
from app.models.rental_plan import RentalPlan
from app.repositories.rental_plan_repository import RentalPlanRepository
from app.services.rental_plan_service import RentalPlanService
from app.repositories.rental_repository import RentalRepository
from app.repositories.motorcycle_repository import MotorcycleRepository
from datetime import date
from app.repositories.user_repository import UserRepository
from app.schemas.rental import RentalReturnResponse

class RentalService:

    @staticmethod
    def _validate_user(db: Session, user_id: int):
        if not UserRepository.get_by_id(db, user_id):
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found.",
                status_code = status.HTTP_404_NOT_FOUND,
            ) 

    @staticmethod   
    def _validate_motorcycle(db: Session, motorcycle_id: int):
        if not MotorcycleRepository.get_by_id(db, motorcycle_id):
            raise AppException(
                error = "MOTORCYCLE_NOT_FOUND", 
                message = "Motorcycle not found.",
                status_code = status.HTTP_404_NOT_FOUND,
            )

    @staticmethod
    def _validate_motorcycle_availability(db: Session, motorcycle_id: int):
        if RentalRepository.has_active_rental(db, motorcycle_id):
            raise AppException(
                error = "MOTORCYCLE_ALREADY_RENTED", 
                message = "Motorcycle is already rented.",
                status_code = status.HTTP_409_CONFLICT,
            )
        
    @staticmethod
    def _validate_license(db: Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)
        
        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found",
                status_code = status.HTTP_404_NOT_FOUND 
            )

        if "A" not in (user.cnh_type):
            raise AppException(
                error = "INVALID_CNH_TYPE",
                message = "User does not have a valid motorcycle driver's license (CNH A).",
                status_code = status.HTTP_403_FORBIDDEN
            )

    @staticmethod
    def _validate_start_date(start_date: date):
        if start_date < date.today():
            raise AppException(
                error = "INVALID_START_DATE", 
                message = "Start date cannot be in the past.",
                status_code = status.HTTP_400_BAD_REQUEST,
            )
        
    @staticmethod
    def register(db: Session, user_id: int, data) -> Rental:

        RentalService._validate_user(db, user_id)
        RentalService._validate_license(db, user_id)
        RentalService._validate_motorcycle(db, data.motorcycle_id)
        RentalService._validate_motorcycle_availability(db, data.motorcycle_id)
        RentalService._validate_start_date(data.start_date)

        plan = RentalPlanRepository.get_by_days(db, data.plan_days)

        if not plan:
            raise AppException(
                error = "RENTAL_PLAN_NOT_FOUND",
                message = "Rental plan not found",
                status_code = status.HTTP_404_NOT_FOUND
            )

        if (data.expected_end_date - data.start_date).days != plan.days:
            raise AppException(
                error = "PLAN_DATA_MISMATCH",
                message = "Dates do not match the rental plan.",
                status_code = status.HTTP_400_BAD_REQUEST  
            )

        rental = Rental(
            user_id = user_id,
            motorcycle_id = data.motorcycle_id,
            start_date = data.start_date,
            expected_end_date = data.expected_end_date,
            end_date = None,
            status = "active"
        )
        return RentalRepository.create(db, rental)

    @staticmethod
    def list_all(db: Session) -> list[Rental]:
        return RentalRepository.list_all(db)

    @staticmethod
    def list_by_motorcycle(db: Session, motorcycle_id: int) -> list[Rental]:
        rentals = RentalRepository.list_by_motorcycle(db, motorcycle_id)

        if not rentals:
            raise AppException(
                error = "RENTALS_NOT_FOUND",
                message = "No rentals found for this motorcycle.",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return rentals

    @staticmethod
    def list_by_user(db: Session, user_id: int) -> list[Rental]:
        return RentalRepository.list_by_user(db, user_id)
    
    @staticmethod
    def _validate_rental(db: Session, rental_id: int) -> Rental:
        rental = RentalRepository.get_by_id(db, rental_id)

        if not rental:
            raise AppException(
                error = "RENTAL_NOT_FOUND",
                message = "Rental not found.",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return rental

    @staticmethod
    def _validate_rental_ownership(rental: Rental, user_id: int):
        if rental.user_id != user_id:
            raise AppException(
                error = "RENTAL_FORBIDDEN",
                message = "You do not have permission to acess this rental.",
                status_code = status.HTTP_403_FORBIDDEN
            )

    @staticmethod
    def return_rental(db: Session, rental_id: int, user_id:int, return_date: date) -> RentalReturnResponse:

        rental = RentalService._validate_rental(db, rental_id)
        RentalService._validate_rental_ownership(rental, user_id)

        if rental.status != "active":
            raise AppException(
                error = "RENTAL_ALREADY_FINISHED", 
                message = "Rental is already finished.",
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
        plan_days = (rental.expected_end_date - rental.start_date).days
        plan = RentalPlanService.get_by_days(db, plan_days)

        price_per_day = float(plan.price_per_day)
        base_amount = plan_days * price_per_day

        used_days = max((return_date - rental.start_date).days, 0)
        penalty_amount = 0.0
        extra_amount = 0.0 

        if return_date < rental.expected_end_date:
            unused_days = plan_days - used_days

            if plan_days == 7:
                penalty_amount = unused_days * price_per_day * 0.20
            elif plan_days == 15:
                penalty_amount = unused_days * price_per_day * 0.40

            total_amount = (used_days * price_per_day) + penalty_amount

        elif return_date > rental.expected_end_date:
            extra_days = (return_date - rental.expected_end_date).days
            extra_amount = extra_days * 50.00
            total_amount = base_amount + extra_amount

        else:
            total_amount = base_amount

        rental.end_date = return_date
        rental.status = "finished"
        RentalRepository.finished(db, rental)

        return RentalReturnResponse(
            rental_id = rental.id,
            total_days = used_days,
            base_amount = round(base_amount, 2),
            penalty_amount = round(penalty_amount, 2),
            extra_amount = round(extra_amount, 2),
            total_amount = round(total_amount, 2)
        )
