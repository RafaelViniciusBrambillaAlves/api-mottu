from fastapi import APIRouter, Depends, status
from app.core.auth import require_admin, get_current_user
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.schemas.motorcycle import MotorcycleResponse, MotorcycleCreate, MotorcycleUpdate
from app.services.motorcycle_service import MotorcycleService
from app.schemas.response import SucessResponse
from app.schemas.error import ErrorResponse

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
            """, 
            responses = {
                403: {"model": ErrorResponse, "description": "Admin access required"},
                409: {"model": ErrorResponse, "description": "VIN already exists"},
                422: {"model": ErrorResponse, "description": "Validation error"},
            })
def create_motorcycle(payload: MotorcycleCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    
    motorcycle = MotorcycleService.register(db, payload)

    return SucessResponse(
        message = "Motorcycle created successfully.",
        data = MotorcycleResponse.model_validate(motorcycle)
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
            """,
            responses = {
                403: {"model": ErrorResponse, "description": "Admin access required"},
            })
def get_motorcycles(db: Session = Depends(get_db), _: User = Depends(require_admin)):

    motorcycles = MotorcycleService.list_all(db)

    return SucessResponse(
        message = "Motorcycles retrieved successfully.",
        data = [MotorcycleResponse.model_validate(m) for m in motorcycles]
    )

@router.get(
            "/available",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[MotorcycleResponse]],
            summary = "List Available Motorcycles",
            description = """
            Retrieves a list of motorcycles that are currently **available for rental**.

            Only motorcycles that are **not associated with an active rental**
            will be returned.

            This endpoint is accessible to **authenticated users**.

            **Authorization:** Authenticated user required.
            """,
            responses = {
                401: {"model": ErrorResponse, "description": "Not authenticated"},
                403: {"model": ErrorResponse, "description": "Invalid credentials"},
            })
def list_available_motorcycles(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    motorcycles = MotorcycleService.list_available(db)

    return SucessResponse(
        message = "Available motorcycles retrieved successfully.",
        data = [MotorcycleResponse.model_validate(m) for m in motorcycles]
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
            """,
            responses = {
                403: {"model": ErrorResponse, "description": "Admin access required"},
                404: {"model": ErrorResponse, "description": "Motorcycle not found"},
            })
def get_motorcycles_by_vin(vin: str, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    
    motorcycle = MotorcycleService.get_by_vin(db, vin)

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
            """,
            responses = {
                403: {"model": ErrorResponse, "description": "Admin access required"},
                404: {"model": ErrorResponse, "description": "Motorcycle not found"},
                409: {"model": ErrorResponse, "description": "VIN already exists"},
            })
def update_motorcycle_vin(motorcycle_id: int, payload: MotorcycleUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):

    motorcycle = MotorcycleService.update_vin(db, motorcycle_id, payload.vin)

    return SucessResponse(
        message = "Motorcycle VIN updated successfully.",
        data = MotorcycleResponse.model_validate(motorcycle)
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
               """,
               responses = {
                403: {"model": ErrorResponse, "description": "Admin access required"},
                404: {"model": ErrorResponse, "description": "Motorcycle not found"},
                409: {"model": ErrorResponse, "description": "Motorcycle has rental records"},
            })
def  delete_motorcycle(motorcycle_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    MotorcycleService.delete(db, motorcycle_id)

    return SucessResponse(
        message = "Motorcycle removed successfully.",
        data = None 
    )