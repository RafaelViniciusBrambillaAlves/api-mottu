from fastapi import APIRouter, Depends, status
from app.core.auth import require_admin, get_current_user
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.schemas.motocycle import MotorcycleResponse, MotorcycleCreate, MotorcycleUpdate
from app.services.motorcycle_service import register_motorcycle, list_motorcycles_service, get_motorcycle_by_vin_service, update_motorcycle_vin_service, list_available_motorcycles_service
from app.schemas.response import SucessResponse

router = APIRouter(prefix = "/motorcycles", tags = ["motorcycles"]) 

@router.post(
            "/", 
            status_code = status.HTTP_201_CREATED, 
            response_model = SucessResponse[MotorcycleResponse]
             )
def create_motorcycle(motorcycle: MotorcycleCreate, db: Session = Depends(get_db), current_admin: User = Depends(require_admin)):
    
    created_motorcycle  = register_motorcycle(db, motorcycle)

    return SucessResponse(
        message = "Motorcycle created successfully.",
        data = MotorcycleResponse.model_validate(created_motorcycle, from_attributes=True)
    )

@router.get(
            "/", 
            status_code = status.HTTP_200_OK, 
            response_model = SucessResponse[list[MotorcycleResponse]]
            )
def get_motorcycles(db: Session = Depends(get_db), _: User = Depends(require_admin)):

    motorcycles = list_motorcycles_service(db)

    return SucessResponse(
        message = "Motorcycles retrieved successfully.",
        data = [MotorcycleResponse.model_validate(motorcycle, from_attributes=True) for motorcycle in motorcycles]
    )

@router.get(
            "/available",
            response_model = SucessResponse[list[MotorcycleCreate]],
            status_code = status.HTTP_200_OK
)
def list_available_motorcycles(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    motorcycles = list_available_motorcycles_service(db)

    return SucessResponse(
        message = "Available motorcycles retrieved successfully.",
        data = motorcycles
    )

@router.get(
            '/{vin}', 
            status_code = status.HTTP_200_OK, 
            response_model = SucessResponse[MotorcycleResponse]
            )
def get_motorcycles_by_vin(vin: str, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    
    motorcycle = get_motorcycle_by_vin_service(db, vin)

    return SucessResponse(
        message = "Motorcycle retrieved successfully.",
        data = MotorcycleResponse.model_validate(motorcycle, from_attributes=True)
    )

@router.patch(
              '/{vin}', 
              status_code = status.HTTP_200_OK, 
              response_model = SucessResponse[MotorcycleResponse]
              )
def update_motorcycle_vin(vin: str, payload: MotorcycleUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):

    motorcyle = update_motorcycle_vin_service(db = db, vin = vin, new_vin = payload.vin)

    return SucessResponse(
        message = "Motorcycle VIN updated successfully.",
        data = MotorcycleResponse.model_validate(motorcyle, from_attributes=True)
    )

