import json
from repository import cache_repository
from repository.database import database
from repository.user_repository import get_by_id
from datetime import datetime
from decimal import Decimal

ORDERS_TABLE_NAME = "orders"
ORDERS_ITEMS_TABLE_NAME = "order_items"
TEMP_ORDER_CACHE_ID = "temp_order"
ORDERS_CACHE_ID = "orders"


async def get_temp_order(user_id):
    cache_id = TEMP_ORDER_CACHE_ID + f"_{user_id}"
    if cache_repository.is_key_exists(cache_id):
        cached_data = cache_repository.get_cache_entity(cache_id)
        return json.loads(cached_data)

    order_query = f"""
        SELECT o.*, oi.item_id, i.name, i.price, oi.quantity
        FROM {ORDERS_TABLE_NAME} o
        LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
        LEFT JOIN items i ON oi.item_id = i.item_id
        WHERE o.user_id = :user_id AND o.status = 'TEMP'
    """
    results = await database.fetch_all(order_query, values={"user_id": user_id})

    if not results:
        return None
    orders = translate_order_to_dictionary(results)
    order_json = json.dumps(list(orders.values())[0])
    cache_repository.update_cache_entity(cache_id, order_json)

    if orders:
        return list(orders.values())[0]
    return None


async def get_orders_history(user_id):
    cache_id = ORDERS_CACHE_ID + f"_{user_id}"
    if cache_repository.is_key_exists(cache_id):
        cached_data = cache_repository.get_cache_entity(cache_id)
        return json.loads(cached_data)

    order_query = f"""
        SELECT o.*, oi.item_id, i.name, i.price, oi.quantity
        FROM {ORDERS_TABLE_NAME} o
        LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
        LEFT JOIN items i ON oi.item_id = i.item_id
        WHERE o.user_id = :user_id AND o.status = 'CLOSE'
    """
    results = await database.fetch_all(order_query, values={"user_id": user_id})

    if not results:
        return None

    orders = translate_order_to_dictionary(results)
    orders_list = list(orders.values())
    orders_json = json.dumps(orders_list)
    cache_repository.update_cache_entity(cache_id, orders_json)

    return list(orders.values())


async def add_item(user_id, item_id):
    temp_order = await get_temp_order(user_id)
    cache_id = TEMP_ORDER_CACHE_ID + f"_{user_id}"

    if temp_order:
        insert_query = f"""
            INSERT INTO {ORDERS_ITEMS_TABLE_NAME} (order_id, item_id, quantity)
            VALUES (:order_id, :item_id, :quantity)
            ON DUPLICATE KEY UPDATE quantity = quantity + :quantity
        """
        insert_values = {
            "order_id": temp_order["order_id"],
            "item_id": item_id,
            "quantity": 1
        }
        await database.execute(insert_query, insert_values)

        fetch_query = f"""
            SELECT o.*, oi.item_id, i.name, i.price, oi.quantity
            FROM {ORDERS_TABLE_NAME} o
            LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
            LEFT JOIN items i ON oi.item_id = i.item_id
            WHERE o.order_id = :order_id
        """
        fetch_values = {"order_id": temp_order["order_id"]}
        result = await database.fetch_all(fetch_query, fetch_values)

        orders = translate_order_to_dictionary(result)
        order = list(orders.values())[0]
        order_json = json.dumps(order)
        cache_repository.update_cache_entity(cache_id, order_json)

        return {"status": "success", "message": "Item added to order.", "order": order}
    else:
        user = await get_by_id(user_id)
        if user is None:
            return {"status": "failed", "message": "User invalid."}

        insert_order_query = f"""
            INSERT INTO {ORDERS_TABLE_NAME} (user_id, shipping_address)
            VALUES (:user_id, :shipping_address)
        """
        insert_order_values = {
            "user_id": user_id,
            "shipping_address": f"{user.address_country}, {user.address_city}"
        }
        new_order_id = await database.execute(insert_order_query, values=insert_order_values)

        insert_item_query = f"""
            INSERT INTO {ORDERS_ITEMS_TABLE_NAME} (order_id, item_id, quantity)
            VALUES (:order_id, :item_id, :quantity)
        """
        insert_item_values = {
            "order_id": new_order_id,
            "item_id": item_id,
            "quantity": 1
        }
        await database.execute(insert_item_query, values=insert_item_values)

        select_order_query = f"""
            SELECT o.*, oi.item_id, i.name, i.price, oi.quantity
            FROM {ORDERS_TABLE_NAME} o
            LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
            LEFT JOIN items i ON oi.item_id = i.item_id
            WHERE o.order_id = :order_id
        """
        select_order_values = {"order_id": new_order_id}
        result = await database.fetch_one(select_order_query, values=select_order_values)
        order = translate_order_to_dictionary(result)
        order_json = json.dumps(list(order.values())[0])
        cache_repository.update_cache_entity(cache_id, order_json)
        return {"status": "success", "message": "New order created and item added."}


async def remove_item(user_id, order_id, item_id):
    cache_id = TEMP_ORDER_CACHE_ID + f"_{user_id}"

    delete_query = f"""
        DELETE FROM {ORDERS_ITEMS_TABLE_NAME}
        WHERE order_id = :order_id AND item_id = :item_id
    """
    delete_values = {"order_id": order_id, "item_id": item_id}
    await database.execute(delete_query, delete_values)

    count_query = f"""
        SELECT COUNT(*) as item_count
        FROM {ORDERS_ITEMS_TABLE_NAME}
        WHERE order_id = :order_id
    """
    count_values = {"order_id": order_id}
    item_count_result = await database.fetch_one(count_query, count_values)
    item_count = item_count_result["item_count"] if item_count_result else 0

    if item_count == 0:
        delete_order_query = f"""
               DELETE FROM {ORDERS_TABLE_NAME}
               WHERE order_id = :order_id;              
           """
        await database.execute(delete_order_query, values={"order_id": order_id})
        cache_repository.remove_cache_entity(cache_id)
    else:
        select_order_query = f"""
                    SELECT o.*, oi.item_id, i.name, i.price, oi.quantity
                    FROM {ORDERS_TABLE_NAME} o
                    LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
                    LEFT JOIN items i ON oi.item_id = i.item_id
                    WHERE o.order_id = :order_id
                """
        result = await database.fetch_all(select_order_query, values={"order_id": order_id})
        order = translate_order_to_dictionary(result)
        order_json = json.dumps(list(order.values())[0])
        cache_repository.update_cache_entity(cache_id, order_json)

        return {"status": "success", "message": "Item removed and order updated.", "order": order}


async def confirm_order(temp_order):
    temp_cache_id = TEMP_ORDER_CACHE_ID + f"_{temp_order.get('user_id')}"
    close_cache_id = ORDERS_CACHE_ID + f"_{temp_order.get('user_id')}"

    query = f"""
            UPDATE {ORDERS_TABLE_NAME}
            SET status = 'CLOSE', created_at = CURRENT_TIMESTAMP
            WHERE order_id = :order_id
        """
    values = {"order_id": temp_order["order_id"]}
    await database.execute(query, values)

    cache_repository.remove_cache_entity(temp_cache_id)

    order_query = f"""
            SELECT o.*, oi.item_id, i.name, i.price, oi.quantity
            FROM {ORDERS_TABLE_NAME} o
            LEFT JOIN {ORDERS_ITEMS_TABLE_NAME} oi ON o.order_id = oi.order_id
            LEFT JOIN items i ON oi.item_id = i.item_id
            WHERE o.user_id = :user_id AND o.status = 'CLOSE'
        """
    results = await database.fetch_all(order_query, values={"user_id": temp_order.get('user_id')})

    orders = translate_order_to_dictionary(results)
    orders_list = list(orders.values())
    orders_json = json.dumps(orders_list)
    cache_repository.update_cache_entity(close_cache_id, orders_json)

    return {"status": "success", "message": "Order confirmed."}


def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)  # or str(value) if you prefer
    elif isinstance(value, datetime):
        return value.isoformat()
    return value


def translate_order_to_dictionary(data):
    orders = {}
    if not isinstance(data, list):
        data = [data]

    for row in data:
        order_id = row["order_id"]
        if order_id not in orders:
            orders[order_id] = {
                "order_id": row["order_id"],
                "user_id": row["user_id"],
                "status": row["status"],
                "created_at": row["created_at"].isoformat() if isinstance(row["created_at"], datetime) else row[
                    "created_at"],
                "shipping_address": row["shipping_address"],
                "items": [],
            }
        if row["item_id"]:
            orders[order_id]["items"].append({
                "item_id": row["item_id"],
                "name": row["name"],
                "price": serialize_value(row["price"]),
                "quantity": row["quantity"],
            })

    return orders
