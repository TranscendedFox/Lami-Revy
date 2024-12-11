from datetime import datetime
from typing import List
from pydantic import BaseModel, condecimal, constr
from model.order_item import OrderItem


class Order(BaseModel):
    order_id: int
    user_id: int
    created_at: datetime = datetime.now()
    shipping_address: constr(max_length=255)
    status: constr(regex=r"TEMP|CLOSE") = "TEMP"
    items: List[OrderItem] = []
