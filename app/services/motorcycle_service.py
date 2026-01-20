from fastapi import status
from sqlalchemy.orm import Session
from app.schemas.motorcycle import MotorcycleCreate
from app.models.motorcycle import Motorcycle
from app.repositories.motorcycle_repository import MotorcycleRepository
from app.core.exceptions import AppException
from datetime import datetime
import re
from app.models.rental import Rental

VIN_REGEX = re.compile(r"^[A-Z]{3}-\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$")

class MotorcycleService:

    @staticmethod
    def _validate_vin_format(vin: str):
        if not VIN_REGEX.match(vin):
            raise AppException(
                error = "INVALID_VIN_FORMAT",
                message = "The VIN format is invalid.",
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod
    def _validate_year(year: int):
        if year < 1900 or year > datetime.now().year + 1:
            raise AppException(
                error = "INVALID_YEAR",
                message = "The year provided is not valid for a motorcycle.",
                status_code = status.HTTP_400_BAD_REQUEST
            )
    
    @staticmethod
    def _validate_unique_vin(db: Session, vin: str):
        if MotorcycleRepository.get_by_vin(db, vin):
            raise AppException(
                error = "VIN_ALREADY_EXISTS",
                message = "A motorcycle with this VIN already exists.",
                status_code = status.HTTP_409_CONFLICT
            )

    @staticmethod
    def _validate_exists(db: Session, motorcycle_id: int) ->  Motorcycle:
        motorcycle = MotorcycleRepository.get_by_id(db, motorcycle_id)
        if not motorcycle:
            raise AppException(
                error = "MOTORCYCLE_NOT_FOUND",
                message = "Motorcycle not found.",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return motorcycle

    @staticmethod
    def register(db: Session, payload: MotorcycleCreate) -> Motorcycle:

        MotorcycleService._validate_vin_format(payload.vin)
        MotorcycleService._validate_unique_vin(db, payload.vin)
        MotorcycleService._validate_year(payload.year)

        motorcycle = Motorcycle(
            model  = payload.model,
            year = payload.year,
            vin = payload.vin
        )

        return MotorcycleRepository.create(db, motorcycle)

    @staticmethod
    def list_all(db: Session):
        return MotorcycleRepository.list_all(db)
    
    @staticmethod
    def list_available(db: Session): 
        motorcycles = MotorcycleRepository.list_available(db)

        if not motorcycles:
            raise AppException(
                error = "NO_AVAILABLE_MOTORCYCLES",
                message = "There are no available motorcycles at the moment.",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return motorcycles
    
    @staticmethod
    def get_by_vin(db: Session, vin: int) -> Motorcycle:
        motorcycle = MotorcycleRepository.get_by_vin(db, vin)

        if not motorcycle:
            raise AppException(
                error = "MOTORCYCLE_NOT_FOUND", 
                message = "Motorcycle for found for this provided VIN.",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return motorcycle

    @staticmethod
    def update_vin(db: Session, motorcycle_id: int, new_vin: str) -> Motorcycle:
        motorcycle = MotorcycleService._validate_exists(db, motorcycle_id)
        
        if motorcycle.vin == new_vin:
            raise AppException(
                error="VIN_NOT_CHANGED",
                message="The new VIN is the same as the current VIN.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        

        MotorcycleService._validate_vin_format(new_vin)
        MotorcycleService._validate_unique_vin(db, new_vin)

        return MotorcycleRepository.update_vin(db, motorcycle, new_vin)

    def delete(db: Session, motorcycle_id: int) -> None:
        motorcycle = MotorcycleService._validate_exists(db, motorcycle_id)
        
        if MotorcycleRepository.has_rentals(db, motorcycle_id):
            raise AppException(
                error = "MOTORCYCLE_HAS_RENTALS",
                message = "Motorcycle cannot be removed because it has rental records.",
                status_code = status.HTTP_409_CONFLICT
            )

        MotorcycleRepository.delete(db, motorcycle)

    
