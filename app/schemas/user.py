from datetime import date
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str = Field(..., min_length = 1, max_length = 50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length = 6)

    cnpj: str = Field(..., min_length = 14, max_length = 20)
    birthday: date
    cnh_number: str = Field(..., min_length = 5, max_length = 20)
    cnh_type: str = Field(..., min_length = 1, max_length = 5)
    
class AdminCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int 
    role: str

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True