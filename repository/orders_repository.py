import json
# from repository import cache_repository
from repository.database import database
from repository.user_repository import get_by_id
from repository.items_repository import get_items_by_list, reduce_item_quantity

ORDERS_TABLE_NAME = "orders"
ORDERS_ITEMS_TABLE_NAME = "order_items"
TEMP_ORDER_CACHE_ID = "temp_order"
ORDERS_CACHE_ID = "orders"


async def get_temp_order(user_id):
    query = f"""
        SELECT o.*, 
               JSON_ARRAYAGG(
                   JSON_OBJECT(
                       'item_id', i.item_id,
                       'name', i.name,
                       'price', i.price,
                       'quantity', oi.quantity
                   )
               ) AS items
        FROM {ORDERS_TABLE_NAME} o
        LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
        LEFT JOIN items i ON oi.item_id = i.item_id
        WHERE o.user_id = :user_id AND o.status = 'TEMP'
        GROUP BY o.order_id
    """
    temp_result = await database.fetch_one(query, values={"user_id": user_id})
    if temp_result:
        temp_order = dict(temp_result)
        temp_order["items"] = json.loads(temp_order["items"]) if temp_order["items"] else []
        return temp_result
    return None


async def get_orders_history(user_id):
    query = f"""
        SELECT o.*, 
               JSON_ARRAYAGG(
                   JSON_OBJECT(
                       'item_id', i.item_id,
                       'name', i.name,
                       'price', i.price,
                       'quantity', oi.quantity
                   )
               ) AS items
        FROM {ORDERS_TABLE_NAME} o
        LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
        LEFT JOIN items i ON oi.item_id = i.item_id
        WHERE o.user_id = :user_id AND o.status = 'CLOSE'
        GROUP BY o.order_id
    """
    close_results = await database.fetch_all(query, values={"user_id": user_id})

    if close_results:
        close_orders = []
        for order in close_results:
            order_dict = dict(order)
            order_dict["items"] = json.loads(order_dict["items"]) if order_dict["items"] else []
            close_orders.append(order_dict)
        return close_orders
    return None


async def add_item(user_id, item_id):
    temp_order = await get_temp_order(user_id)

    if temp_order:
        query = f"""
            INSERT INTO {ORDERS_ITEMS_TABLE_NAME} (order_id, item_id, quantity)
            VALUES (:order_id, :item_id, :quantity)
            ON DUPLICATE KEY UPDATE quantity = quantity + 1"""

        values = {
            "order_id": temp_order.order_id,
            "item_id": item_id,
            "quantity": 1
        }
        await database.execute(query, values)
        return {"status": "success", "message": "Item added to order."}
    else:
        user = await get_by_id(user_id)
        if user is None:
            return {"status": "failed", "message": "User invalid."}

        query = f"""
                INSERT INTO {ORDERS_TABLE_NAME} (user_id, shipping_address)
                VALUES (:user_id, :shipping_address)
            """
        values = {
            "user_id": user_id,
            "shipping_address": f"{user.address_country}, {user.address_city}"
        }
        new_order_id = await database.execute(query, values)

        query = f"""
                INSERT INTO {ORDERS_ITEMS_TABLE_NAME} (order_id, item_id, quantity)
                VALUES (:order_id, :item_id, :quantity)
            """
        values = {
            "order_id": new_order_id,
            "item_id": item_id,
            "quantity": 1
        }
        await database.execute(query, values)
        return {"status": "success", "message": "New order created and item added."}


async def remove_item(order_id, item_id):
    query = f"""
        DELETE FROM {ORDERS_ITEMS_TABLE_NAME}
        WHERE order_id = :order_id AND item_id = :item_id"""
    values = {"order_id": order_id, "item_id": item_id}
    await database.execute(query, values)
    # await update_cache(user_id)


async def confirm_order(user_id):
    temp_order = await get_temp_order(user_id)
    if temp_order is None:
        return {"status": "failed", "message": "Temp order invalid."}

    items = json.loads(temp_order.items)
    items_ids = []
    for item in items:
        items_ids.append(int(item['item_id']))

    items_in_database = await get_items_by_list(items_ids)
    for order_item in items:
        item_in_db = next((item for item in items_in_database if item.item_id == order_item["item_id"]), None)

        if not item_in_db:
            return {"status": "failed", "message": f"Item {order_item['item_id']} not found in stock."}

        if item_in_db.stock < order_item["quantity"]:
            return {
                "status": "failed",
                "message": f"Insufficient stock for item {order_item.item_id} (available: {item_in_db['stock']}, requested: {order_item.quantity})."
            }

    for order_item in items:
        await reduce_item_quantity(order_item["item_id"], order_item["quantity"])

    query = f"""
            UPDATE {ORDERS_TABLE_NAME}
            SET status = 'CLOSE', created_at = CURRENT_TIMESTAMP
            WHERE order_id = :order_id
        """
    values = {"order_id": temp_order.order_id}
    await database.execute(query, values)

    return {"status": "success", "message": "Order confirmed."}
