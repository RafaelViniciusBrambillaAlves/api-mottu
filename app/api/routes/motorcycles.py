from fastapi import APIRouter, Depends, status
from app.core.auth import require_admin, get_current_user
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.schemas.motocycle import MotorcycleResponse, MotorcycleCreate, MotorcycleUpdate
from app.services.motorcycle_service import (register_motorcycle, list_motorcycles_service, get_motorcycle_by_vin_service, 
                                             update_motorcycle_vin_service, list_available_motorcycles_service, delete_motorcycle_service)
from app.schemas.response import SucessResponse

router = APIRouter(prefix = "/motorcycles", tags = ["motorcycles"]) 

@router.post(
            "/", 
            status_code = status.HTTP_201_CREATED, 
            response_model = SucessResponse[MotorcycleResponse],
            summary = "Create a Motorcycle",
            description = """
            Creates a new motorcycle in the system.

            This endpoint is restricted to **administrators only**.
            The motorcycle will be registered using the provided VIN and metadata.

            **Authorization:** Admin required.
            """
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
            response_model = SucessResponse[list[MotorcycleResponse]],
            summary = "List all Motorcycles",
            description = """
            Retrieves a list of all motorcycles registered in the system.

            This endpoint is restricted to **administrators only** and returns
            both available and rented motorcycles.

            **Authorization:** Admin required.
            """
            )
def get_motorcycles(db: Session = Depends(get_db), _: User = Depends(require_admin)):

    motorcycles = list_motorcycles_service(db)

    return SucessResponse(
        message = "Motorcycles retrieved successfully.",
        data = [MotorcycleResponse.model_validate(motorcycle, from_attributes=True) for motorcycle in motorcycles]
    )

@router.get(
            "/available",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[MotorcycleCreate]],
            summary = "List Available Motorcycles",
            description = """
            Retrieves a list of motorcycles that are currently **available for rental**.

            Only motorcycles that are **not associated with an active rental**
            will be returned.

            This endpoint is accessible to **authenticated users**.

            **Authorization:** Authenticated user required.
            """     
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
            response_model = SucessResponse[MotorcycleResponse],
            summary = "Get Motorcycle by VIN",
            description = """
            Retrieves detailed information about a motorcycle using its VIN.

            This endpoint is restricted to **administrators only**.

            **Path parameters:**
            - **vin**: Vehicle Identification Number of the motorcycle.

            **Authorization:** Admin required.
            """
            )
def get_motorcycles_by_vin(vin: str, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    
    motorcycle = get_motorcycle_by_vin_service(db, vin)

    return SucessResponse(
        message = "Motorcycle retrieved successfully.",
        data = MotorcycleResponse.model_validate(motorcycle, from_attributes=True)
    )

@router.patch(
            '/{motorcycle_id}', 
            status_code = status.HTTP_200_OK, 
            response_model = SucessResponse[MotorcycleResponse],
            summary = "Update Motorcycle VIN",
            description = """
            Updates the VIN of an existing motorcycle using its ID.

            This endpoint allows administrators to update the VIN
            associated with a motorcycle.

            **Path parameters:**
            - **motorcycle_id**: Unique identifier of the motorcycle

            **Authorization:** Admin required.
            """
              )
def update_motorcycle_vin(motorcycle_id: int, payload: MotorcycleUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):

    motorcyle = update_motorcycle_vin_service(db, motorcycle_id, payload.vin)

    return SucessResponse(
        message = "Motorcycle VIN updated successfully.",
        data = MotorcycleResponse.model_validate(motorcyle, from_attributes=True)
    )

@router.delete(
                "/{motorcycle_id}",
                status_code = status.HTTP_200_OK,
                response_model = SucessResponse[None],
                summary = "Delete a motorcycle",
                description = """
                Removes a motorcycle from the system.

                **Business rules:**
                - Motorcycle must exist
                - Motorcycle must NOT have any rental records
                - Only administrators can perform this action

                **Path parameters:**
                - **motorcycle_id**: Unique identifier of the motorcycle

                **Authorization:** Admin required.
                """
)
def  delete_motorcycle(motorcycle_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    delete_motorcycle_service(db, motorcycle_id)

    return SucessResponse(
        message = "Motorcycle removed successfully.",
        data = None 
    )