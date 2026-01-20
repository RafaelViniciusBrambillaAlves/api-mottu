from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.rental import Rental 
from app.models.rental_plan import RentalPlan
from app.repositories.rental_repository import create_rental, get_rental_by_id, get_plan_by_days, finished_rental
from app.repositories.motorcycle_repository import get_motorcycle_by_id
from app.models.user import User
from app.models.motorcycle import Motorcycle
from datetime import date
from app.core.exceptions import AppException
from app.repositories.user_repository import get_user_by_id

def _validate_user(db: Session, user_id: int) -> None:
    exists = get_user_by_id(db, user_id)

    if not exists:
        raise AppException(
            error = "USER_NOT_FOUND",
            message = "User not found.",
            status_code = status.HTTP_404_NOT_FOUND,
        ) 

def _validate_plan(db: Session, plan_days) -> RentalPlan:
    plan = db.query(RentalPlan).filter(RentalPlan.days == plan_days).first()
    
    if not plan:
        raise AppException(
            error = "INVALID_RENTAL_PLAN",
            message = "Invalid rental plan.",
            status_code = status.HTTP_400_BAD_REQUEST,
        )   
    return plan

def _validate_motorcycle(db: Session, motorcycle_id: int) -> None:
    if not get_motorcycle_by_id(db, motorcycle_id):
        raise AppException(
            error = "MOTORCYCLE_NOT_FOUND", 
            message = "Motorcycle not found.",
            status_code = status.HTTP_404_NOT_FOUND,
        )

def _validate_motorcycle_availability(db: Session, motorcycle_id: int) -> None:
    active_rental = db.query(Rental).filter(Rental.motorcycle_id == motorcycle_id, Rental.status == "active").first()

    if active_rental:
        raise AppException(
            error = "MOTORCYCLE_ALREADY_RENTED", 
            message = "Motorcycle is already rented.",
            status_code = status.HTTP_409_CONFLICT,
        )

def _validate_start_date(start_date: date) -> None:
    if start_date < date.today():
        raise AppException(
            error = "INVALID_START_DATE", 
            message = "Start date cannot be in the past.",
            status_code = status.HTTP_400_BAD_REQUEST,
        )
    
def _validate_dates_against_plan(start_date: date, expected_end_date: date, plan_days: date) -> None:
    real_days = (expected_end_date - start_date).days

    if real_days != plan_days:
        raise AppException(
            error = "PLAN_DATES_MISMATCH",
            message = "Dates do not match the selected rental plan.",
            status_code = status.HTTP_400_BAD_REQUEST
        )

def _validate_user_has_motorcycle_license(db: Session, user_id) -> None:
    user = get_user_by_id(db, user_id)
    
    if not user:
        raise AppException(
            error = "USER_NOT_FOUND",
            message = "User not found.",
            status_code = status.HTTP_404_NOT_FOUND
        )

    if not user.cnh_type:
        raise AppException(
            error = "CNH_NOT_INFORMED",
            message = "User does not have a driver's license registered.",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    
    if "A" not in user.cnh_type:
        raise AppException(
            error = "INVALID_CNH_TYPE",
            message = "User does not have a valid motorcycle driver's license (CNH A).",
            status_code = status.HTTP_403_FORBIDDEN
        )
    
def _validate_end_date_on_creation(end_date):
    if end_date not in (None, ""):
        raise AppException(
            error = "END_DATE_NOT_ALLOWED",
            message = "End date cannot be set when creating a rental.",
            status_code = status.HTTP_400_BAD_REQUEST
        )

def register_rental(db: Session, user_id: int, data):

    _validate_user(db, user_id)
    _validate_motorcycle(db, data.motorcycle_id)
    _validate_motorcycle_availability(db, data.motorcycle_id)
    _validate_start_date(data.start_date)
    _validate_user_has_motorcycle_license(db, user_id)
    _validate_end_date_on_creation(data.end_date)

    plan = _validate_plan(db, data.plan_days)

    _validate_dates_against_plan(data.start_date, data.expected_end_date, plan.days)

    rental = Rental(
        user_id = user_id,
        motorcycle_id = data.motorcycle_id,
        start_date = data.start_date,
        expected_end_date = data.expected_end_date,
        end_date = None,
        status = "active"
    )

    return create_rental(db, rental)

def list_all_rentals_service(db: Session) -> list[Rental]:
    return db.query(Rental).all()

def list_rentals_by_motorcycle_service(db: Session, motorcycle_id: int) -> list[Rental]:
    rentals = db.query(Rental).filter(Rental.motorcycle_id == motorcycle_id).all()

    if not rentals:
        raise AppException(
            error = "RENTALS_NOT_FOUND",
            message = "No rentals found for this motorcycle.",
            status_code = status.HTTP_404_NOT_FOUND
        )
    return rentals

def list_user_rentals_service(db: Session, user_id: int) -> list[Rental]:
    return db.query(Rental).filter(Rental.user_id == user_id).all()

def _validate_rental(db: Session, rental_id: int) -> Rental:
    rental = get_rental_by_id(db, rental_id)

    if not rental:
        raise AppException(
            error = "RENTAL_NOT_FOUND",
            message = "Rental not found.",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    return rental

def _validate_rental_ownership(rental: Rental, user_id: int) -> None:
    if rental.user_id != user_id:
        raise AppException(
            error = "RENTAL_FORBIDDEN",
            message = "You do not have permission to acess this rental.",
            status_code = status.HTTP_403_FORBIDDEN
        )

def _validate_rental_plan(db: Session, plan_days: int) -> RentalPlan:
    plan = get_plan_by_days(db, plan_days)

    if not plan: 
        raise AppException(
            error = "RENTAL_PLAN_NOT_FOUND", 
            message = "Rental plan not found.",
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return plan

def return_rental_service(db: Session, rental_id: int, user_id:int, return_date: date):

    rental = _validate_rental(db, rental_id)
    _validate_rental_ownership(rental, user_id)

    if rental.status != "active":
        raise AppException(
            error = "RENTAL_ALREADY_FINISHED", 
            message = "Rental is already finished.",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    
    plan_days = (rental.expected_end_date - rental.start_date).days
    plan = _validate_rental_plan(db, plan_days)

    price_per_day = float(plan.price_per_day)

    user_days = max((return_date - rental.start_date).days, 0)
    base_amount = plan_days * price_per_day

    penalty_amount = 0.0
    extra_amount = 0.0 

    if return_date < rental.expected_end_date:
        unused_days = plan_days - user_days
        daily_amount_used = user_days * price_per_day

        if plan_days == 7:
            penalty_amount = unused_days * price_per_day * 0.20
        elif plan_days == 15:
            penalty_amount = unused_days * price_per_day * 0.40

        total_amount = daily_amount_used + penalty_amount

    elif return_date > rental.expected_end_date:
        extra_days = (return_date - rental.expected_end_date).days
        extra_amount = extra_days * 50.00
        total_amount = base_amount + extra_amount

    else:
        total_amount = base_amount

    rental.end_date = return_date
    rental.status = "finished"

    finished_rental(db, rental)

    return {
        "rental_id": rental.id,
        "total_days": user_days,
        "base_amount": round(base_amount, 2),
        "penalty_amount": round(penalty_amount, 2),
        "extra_amount": round(extra_amount, 2),
        "total_amount": round(total_amount, 2)
    }
