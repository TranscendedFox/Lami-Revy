from pydantic import BaseModel
from typing import Optional
from model.gender_enum import GenderEnum


class User(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address_city: Optional[str] = None
    address_country: Optional[str] = None
    hashed_password: str
    gender: GenderEnum
    age: Optional[int] = None
    annual_income: Optional[float] = None
