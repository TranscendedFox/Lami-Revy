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
    query = f"SELECT * FROM {TABLE_NAME}"
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
