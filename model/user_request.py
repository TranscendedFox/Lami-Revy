from typing import Optional
from pydantic import BaseModel
from model.gender_enum import GenderEnum


class UserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address_city: str
    address_country: str
    password: str
    gender: GenderEnum
    age: Optional[int] = None
    annual_income: Optional[float] = None
