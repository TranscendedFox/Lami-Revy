import json
from typing import Optional, List
from repository import cache_repository
from repository.database import database
from model.item import Item

TABLE_NAME = "items"
ALL_ITEMS_CACHE_ID = "all_items"


async def get_all_items():
    if cache_repository.is_key_exists(ALL_ITEMS_CACHE_ID):
        string_items = cache_repository.get_cache_entity(ALL_ITEMS_CACHE_ID)
        return json.loads(string_items)
    query = f"SELECT * FROM {TABLE_NAME} WHERE stock > 0"
    results = await database.fetch_all(query)
    if results:
        items = [Item(**result) for result in results]
        for item in items:
            item.json()
        items_json = json.dumps([item.dict() for item in items])
        cache_repository.update_cache_entity(ALL_ITEMS_CACHE_ID, items_json)
        return [Item(**result) for result in results]
    else:
        return None


async def get_items_by_search(name_query: Optional[List[str]] = None, conditions: Optional[List[dict]] = None):
    # Base query
    query = f"SELECT * FROM {TABLE_NAME} WHERE 1=1"

    # Add name filter
    if name_query:
        name_conditions = " OR ".join([f"name LIKE :keyword{i}" for i in range(len(name_query))])
        query += f" AND ({name_conditions})"

    # Add conditions for amount and price
    if conditions:
        for condition in conditions:
            field = condition['type']
            operator = condition['operator']
            value = condition['value']

            if field == "amount":
                query += f" AND stock {operator} :stock_value"
            elif field == "price":
                query += f" AND price {operator} :price_value"

    # Prepare query parameters
    params = {}
    if name_query:
        for i, keyword in enumerate(name_query):
            params[f"keyword{i}"] = f"%{keyword.strip()}%"
    for condition in conditions:
        if condition['type'] == "amount":
            params["stock_value"] = condition['value']
        elif condition['type'] == "price":
            params["price_value"] = condition['value']

    # Execute query
    results = await database.fetch_all(query, values=params)
    if results:
        return [Item(**result) for result in results]
    else:
        return None


async def get_items_by_list(items: List[int]):
    placeholders = ", ".join([":item_id_" + str(i) for i in range(len(items))])
    values = {f"item_id_{i}": item_id for i, item_id in enumerate(items)}

    query = f"""
            SELECT * FROM {TABLE_NAME}
            WHERE item_id IN ({placeholders})
        """

    rows = await database.fetch_all(query, values=values)
    return [Item(**row) for row in rows]


async def reduce_item_quantity(item_id, amount):
    query_check_stock = f"""
            SELECT stock FROM {TABLE_NAME}
            WHERE item_id = :item_id
        """
    current_stock = await database.fetch_one(query_check_stock, values={"item_id": item_id})

    if not current_stock or current_stock["stock"] < amount:
        raise ValueError(
            f"Insufficient stock for item_id={item_id}. Available: {current_stock['stock'] if current_stock else 0}, Requested: {amount}")

    query_update_stock = f"""
            UPDATE {TABLE_NAME}
            SET stock = stock - :amount
            WHERE item_id = :item_id
        """
    await database.execute(query_update_stock, values={"amount": amount, "item_id": item_id})


async def update_items_cache():
    if cache_repository.is_key_exists(ALL_ITEMS_CACHE_ID):
        query = f"SELECT * FROM {TABLE_NAME} WHERE stock > 0"
        results = await database.fetch_all(query)
        if results:
            items = [Item(**result) for result in results]
            for item in items:
                item.json()
            items_json = json.dumps([item.dict() for item in items])
            cache_repository.update_cache_entity(ALL_ITEMS_CACHE_ID, items_json)
