from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address_city: str
    address_country: str
    password: str
