from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.rental import RentalCreate, RentalResponse, RentalReturnRequest, RentalReturnResponse
from app.services.rental_service import RentalService
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.response import SucessResponse
from app.core.auth import get_current_user, require_admin
from app.schemas.error import ErrorResponse

router = APIRouter(prefix = "/rentals", tags = ["rentals"])

@router.post(
            "/", 
            status_code = status.HTTP_201_CREATED, 
            response_model = SucessResponse[RentalResponse],
            summary = "Create a rental",
            description = """
            Creates a new motorcycle rental for the authenticated user.

            The rental will be created based on the selected rental plan,
            start date, and motorcycle availability.

            **Business rules applied:**
            - User must be authenticated
            - Motorcycle must exist and be available
            - Rental plan must be valid
            - Start date cannot be in the past

            **Authorization:** Authenticated user required.
            """,
            responses={
                401: {"model": ErrorResponse, "description": "Not authenticated"},
                404: {"model": ErrorResponse, "description": "Motorcycle or rental plan not found"},
                409: {"model": ErrorResponse, "description": "Motorcycle unavailable or invalid rental state"},
                422: {"model": ErrorResponse, "description": "Validation error"},
            })
def create_rental(data: RentalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    created_rental = RentalService.register(db, current_user.id, data)

    return SucessResponse(
        message = "Rental created successfully.",
        data = RentalResponse.model_validate(created_rental)
    )

@router.get(
            "/",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[RentalResponse]],
            summary = "List all rentals",
            description = """
            Retrieves all rentals registered in the system.

            This endpoint is intended for administrative and operational
            purposes, providing visibility over all rentals regardless
            of user or motorcycle.

            **Authorization:** Admin required.
            """,
            responses = {
                403: {"model": ErrorResponse, "description": "Admin access required"},
            })
def list_all_rentals(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    rentals = RentalService.list_all(db)

    return SucessResponse(
        message = "All rentals retrieved successfully.",
        data = [RentalResponse.model_validate(r) for r in rentals]
    )

@router.get(
            "/motorcycle/{motorcycle_id}",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[RentalResponse]],
            summary = "List rentals by motorcycle",
            description = """
            Retrieves all rentals associated with a specific motorcycle.

            This endpoint allows administrators to track the rental history
            of a motorcycle.

            **Path parameters:**
            - **motorcycle_id**: Unique identifier of the motorcycle.

            **Authorization:** Admin required.
            """,
            responses = {
                403: {"model": ErrorResponse, "description": "Admin access required"},
                404: {"model": ErrorResponse, "description": "Motorcycle not found"},
            })
def list_rentals_by_motorcycle(motorcycle_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    rentals = RentalService.list_by_motorcycle(db, motorcycle_id)

    return SucessResponse(
        message = "Rentals for motorcycle retrieved successfully.",
        data = [RentalResponse.model_validate(r) for r in rentals]
    )

@router.get(
            "/me",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[RentalResponse]],
            summary = "List my rentals",
            description = """
            Retrieves all rentals associated with the authenticated user.

            This endpoint returns both active and completed rentals,
            allowing users to view their rental history.

            **Authorization:** Authenticated user required.
            """,
            responses = {
                401: {"model": ErrorResponse, "description": "Not authenticated"},
            })
def list_my_rentals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rentals = RentalService.list_by_user(db, current_user.id)

    return SucessResponse(
        message = "User rentals retrieved successfully.",
        data = [RentalResponse.model_validate(r) for r in rentals]
    )
    
@router.post(
            "/{rental_id}/return",
            status_code = status.HTTP_200_OK, 
            response_model = SucessResponse[RentalReturnResponse],
            summary = "Calculate rental return amount",
            description = """
            Calculates the total rental amount based on the return date.

            **Rules applied:**
            - Early return may generate penalty
            - Late return generates extra daily fee
            - Exact return date charges only base amount

            **Authorization:** Authenticated user required.
            """,
            responses = {
                401: {"model": ErrorResponse, "description": "Not authenticated"},
                403: {"model": ErrorResponse, "description": "Rental does not belong to user"},
                404: {"model": ErrorResponse, "description": "Rental not found"},
                409: {"model": ErrorResponse, "description": "Rental already returned"},
                422: {"model": ErrorResponse, "description": "Validation error"},
            })
def calculate_return(rental_id: int, data: RentalReturnRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = RentalService.return_rental(db, rental_id, current_user.id, data.return_date)

    return SucessResponse(
        message = "Rental amount calculated successfully.",
        data = RentalReturnResponse.model_validate(result)
    )