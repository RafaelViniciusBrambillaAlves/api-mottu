from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.rental import RentalCreate, RentalResponse
from app.services.rental_service import register_rental, list_all_rentals_service, list_rentals_by_motorcycle_service, list_user_rentals_service
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.response import SucessResponse
from app.core.auth import get_current_user, require_admin

router = APIRouter(prefix = "/rentals", tags = ["rentals"])

@router.post(
            "/", 
            status_code = status.HTTP_201_CREATED, 
            response_model = SucessResponse[RentalResponse]
            )
def create_rental(data: RentalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    created_rental = register_rental(db, current_user.id, data)

    return SucessResponse(
        message = "Rental created successfully.",
        data = RentalResponse.model_validate(created_rental, from_attributes = True)
    )

@router.get(
            "/",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[RentalResponse]]
)
def list_all_rentals(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    rentals = list_all_rentals(db)

    return SucessResponse(
        message="All rentals retrieved successfully.",
        data=rentals
    )

@router.get(
            "/motorcycle/{motorcycle_id}",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[RentalResponse]]
)
def list_rentals_by_motorcycle(motorcycle_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    rentals = list_rentals_by_motorcycle_service(db, motorcycle_id)

    return SucessResponse(
        message = "Rentals for motorcycle retrieved successfully.",
        data = rentals 
    )

@router.get(
            "/me",
            status_code = status.HTTP_200_OK,
            response_model = SucessResponse[list[RentalResponse]]
            )
def list_my_rentals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rentals = list_user_rentals_service(db, current_user.id)

    return SucessResponse(
        message = "User rentals retrieved successfully.",
        data = rentals 
    )
    