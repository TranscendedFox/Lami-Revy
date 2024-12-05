from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address_city: str
    address_country: str
    hashed_password: str
