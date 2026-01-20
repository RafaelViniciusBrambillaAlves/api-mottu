from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class RentalCreate(BaseModel):
    motorcycle_id: int
    plan_days: int
    start_date: date
    expected_end_date: date

class RentalResponse(BaseModel):
    id: int 
    motorcycle_id: int
    user_id: int
    start_date: date
    expected_end_date: date
    status: str

    class Config: 
        from_attributes = True


class RentalReturnRequest(BaseModel):
    return_date: date

class RentalReturnResponse(BaseModel):
    rental_id: int
    total_days: int
    base_amount: float
    penalty_amount: float
    extra_amount: float
    total_amount: float

    