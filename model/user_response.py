from typing import Optional
from pydantic import BaseModel
from model.gender_enum import GenderEnum


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address_city: str
    address_country: str
    gender: GenderEnum
    age: Optional[int] = None
    annual_income: Optional[float] = None
