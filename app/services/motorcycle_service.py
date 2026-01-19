from fastapi import status
from sqlalchemy.orm import Session
from app.schemas.motocycle import MotorcycleCreate
from app.models.motorcycle import Motorcycle
from app.repositories.motorcycle_repository import create_motorcycle, get_motorcycle_by_vin, update_motorcycle, geta_available_motorcycle
from app.core.exceptions import AppException
from datetime import datetime
import re

VIN_REGEX = re.compile(r"^[A-Z]{3}-\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$")

def _validate_vin(db: Session, vin: str):
    if get_motorcycle_by_vin(db, vin):
        raise AppException(
            error = "VIN_ALREADY_EXISTS",
            message = "A motorcycle with this VIN already exists.",
            status_code = status.HTTP_409_CONFLICT
        )

def _validate_year(year: int):
    if year < 1900 or year > datetime.now().year + 1:
        raise AppException(
            error = "INVALID_YEAR",
            message = "The year provided is not valid for a motorcycle.",
            status_code = status.HTTP_400_BAD_REQUEST
        )

def _validate_vin_format(vin: str):
    if not VIN_REGEX.match(vin):
        raise AppException(
            error = "INVALID_VIN_FORMAT",
            message = "The VIN format is invalid.",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    
def _validate_exist_motorcycle(db: Session, vin: str) -> Motorcycle:
    motorcycle = get_motorcycle_by_vin(db, vin)

    if not motorcycle:
        raise AppException(
            error = "MOTORCYCLE_NOT_FOUND",
            message = "No motorcycle found with the provided VIN.",
            status_code = status.HTTP_404_NOT_FOUND
        )
    return motorcycle


def register_motorcycle(db: Session, motorcycle: MotorcycleCreate) -> Motorcycle:

    _validate_vin(db, motorcycle.vin)
    _validate_year(motorcycle.year)
    _validate_vin_format(motorcycle.vin)

    new_motorcycle = Motorcycle(
        model  = motorcycle.model,
        year = motorcycle.year,
        vin = motorcycle.vin
    )

    return create_motorcycle(db, new_motorcycle)


def list_motorcycles_service(db: Session) -> list[Motorcycle]:
    return db.query(Motorcycle).all()


def get_motorcycle_by_vin_service(db: Session, vin: str) -> Motorcycle:
    return _validate_exist_motorcycle(db, vin)
   

def update_motorcycle_vin_service(db: Session, vin: str, new_vin: str) -> Motorcycle:
    motorcycle = _validate_exist_motorcycle(db, vin)
    
    if not new_vin:
        raise AppException(
            error="VIN_REQUIRED",
            message="VIN must be provided to update.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if vin == new_vin:
        raise AppException(
            error = "VIN_NOT_CHANGED",
            message = "The new VIN is the same as the current VIN.",
            status_code = status.HTTP_400_BAD_REQUEST
        )
    
    _validate_vin_format(new_vin)
    _validate_vin(db, new_vin)

    return update_motorcycle(db, motorcycle, new_vin)

def list_available_motorcycles_service(db: Session) -> list[Motorcycle]:
    motorcycles = geta_available_motorcycle(db)

    if not motorcycles:
        raise AppException(
            error = "NO_AVAILABLE_MOTORCYCLES", 
            message = "There are no available motorcycles at the moment.",
            status_code = status.HTTP_404_NOT_FOUND
        )
    
    return motorcycles