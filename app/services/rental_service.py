from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.rental import Rental 
from app.models.rental_plan import RentalPlan
from app.repositories.rental_repository import create_rental
from app.models.user import User
from app.models.motorcycle import Motorcycle
from datetime import date
from app.core.exceptions import AppException

def _validate_user(db: Session, user_id: int) -> None:
    exists = db.query(User.id).filter(User.id == user_id).first()

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
    exists = db.query(Motorcycle.id).filter(Motorcycle.id == motorcycle_id).first()

    if not exists:
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



def register_rental(db: Session, user_id: int, data):
    _validate_user(db, user_id)
    _validate_motorcycle(db, data.motorcycle_id)
    _validate_motorcycle_availability(db, data.motorcycle_id)
    _validate_start_date(data.start_date)

    plan = _validate_plan(db, data.plan_days)

    _validate_dates_against_plan(data.start_date, data.expected_end_date, plan.days)

    rental = Rental(
        user_id = user_id,
        motorcycle_id = data.motorcycle_id,
        start_date = data.start_date,
        expected_end_date = data.expected_end_date,
        end_date=data.end_date,
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


