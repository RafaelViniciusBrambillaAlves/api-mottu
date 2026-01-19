from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class RentalCreate(BaseModel):
    motorcycle_id: int
    plan_days: int
    start_date: date
    expected_end_date: date
    end_date: Optional[str] = Field(None)

class RentalResponse(BaseModel):
    id: int 
    motorcycle_id: int
    user_id: int
    start_date: date
    expected_end_date: date
    status: str

    class Config: 
        from_attributes = True
