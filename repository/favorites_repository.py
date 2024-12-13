import json
from repository import cache_repository
from repository.database import database
from model.item import Item

FAVORITES_TABLE_NAME = "favorites"
ITEMS_TABLE_NAME = "items"
FAVORITES_CACHE_ID = "favorites"


async def get_favorites(user_id):
    cache_id = FAVORITES_CACHE_ID + f"_{user_id}"
    if cache_repository.is_key_exists(cache_id):
        string_items = cache_repository.get_cache_entity(cache_id)
        return json.loads(string_items)
    query = f"""
            SELECT items.item_id, items.name, items.price, items.stock
            FROM {FAVORITES_TABLE_NAME}
            JOIN {ITEMS_TABLE_NAME} ON {FAVORITES_TABLE_NAME}.item_id = {ITEMS_TABLE_NAME}.item_id
            WHERE {FAVORITES_TABLE_NAME}.user_id = :user_id
        """
    results = await database.fetch_all(query, values={"user_id": user_id})
    if results:
        items = [Item(**result) for result in results]
        for item in items:
            item.json()
        items_json = json.dumps([item.dict() for item in items])
        cache_repository.update_cache_entity(cache_id, items_json)
        return items
    else:
        return None


async def add_favorite(user_id, item_id):
    query = f"""
    INSERT INTO {FAVORITES_TABLE_NAME} (user_id, item_id)
    VALUES (:user_id, :item_id)"""
    values = {"user_id": user_id, "item_id": item_id}
    await database.execute(query, values)
    await update_favorite_cache(user_id)


async def remove_favorite(user_id, item_id):
    query = f"""
    DELETE FROM {FAVORITES_TABLE_NAME}
    WHERE user_id = :user_id AND item_id = :item_id"""
    values = {"user_id": user_id, "item_id": item_id}
    await database.execute(query, values)
    await update_favorite_cache(user_id)


async def update_favorite_cache(user_id):
    cache_id = FAVORITES_CACHE_ID + f"_{user_id}"
    if cache_repository.is_key_exists(cache_id):
        cache_id = FAVORITES_CACHE_ID + f"_{user_id}"
        query = f"""
                    SELECT items.item_id, items.name, items.price, items.stock
                    FROM {FAVORITES_TABLE_NAME}
                    JOIN {ITEMS_TABLE_NAME} ON {FAVORITES_TABLE_NAME}.item_id = {ITEMS_TABLE_NAME}.item_id
                    WHERE {FAVORITES_TABLE_NAME}.user_id = :user_id
                """
        results = await database.fetch_all(query, values={"user_id": user_id})
        if results:
            items = [Item(**result) for result in results]
            for item in items:
                item.json()
            items_json = json.dumps([item.dict() for item in items])
            cache_repository.update_cache_entity(cache_id, items_json)
        else:
            cache_repository.remove_cache_entity(cache_id)
