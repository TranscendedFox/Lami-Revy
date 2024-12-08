from typing import Optional

from model.user import User
from model.user_request import UserRequest
from repository.database import database

TABLE_NAME = "users"


async def get_by_id(user_id: int) -> Optional[User]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return User(**result)
    else:
        return None


async def get_by_username(username: str) -> Optional[User]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE username=:username"
    result = await database.fetch_one(query, values={"username": username})
    if result:
        print(result)
        # Map tuple to a dictionary with field names
        result_dict = {
            "user_id": result[0],
            "username": result[1],
            "first_name": result[2],
            "last_name": result[3],
            "email": result[4],
            "phone": result[5],
            "address_city": result[6],
            "address_country": result[7],
            "hashed_password": result[8]
        }
        return User(**result_dict)
    else:
        return None


async def create_user(user: UserRequest, hashed_password: str):
    query = f"""
        INSERT INTO {TABLE_NAME} (first_name, last_name, email, phone, address_city, address_country, username, 
        hashed_password) VALUES (:first_name, :last_name, :email, :phone, :address_city, :address_country, :username, 
        :hashed_password)"""
    user_dict = user.dict()
    del user_dict["password"]
    values = {**user_dict, "hashed_password": hashed_password}

    await database.execute(query, values)


async def delete_user_by_id(id: int):
    query = f"DELETE FORM {TABLE_NAME} WHERE id =:user_id"
    await database.execute(query, values={"user_id": id})
