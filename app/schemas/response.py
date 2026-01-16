from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class SucessResponse(BaseModel, Generic[T]):
    sucess: bool = True
    message: str
    data: Optional[T] = None