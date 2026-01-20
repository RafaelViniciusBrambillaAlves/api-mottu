from pydantic import BaseModel, Field
from typing import Optional

class MotorcycleBase(BaseModel):
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)
    vin: str = Field(..., min_length=5, max_length=50)

class MotorcycleCreate(MotorcycleBase):
    pass

class MotorcycleUpdate(BaseModel):
    vin: str = Field(None, min_length=5, max_length=50)

class MotorcycleResponse(MotorcycleBase):
    id: int

    class Config:
        from_attributes = True