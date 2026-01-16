from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str = Field(..., min_length = 1, max_length = 50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length = 6)

class UserResponse(UserBase):
    id: int 

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True