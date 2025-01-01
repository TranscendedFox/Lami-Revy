from repository import orders_repository
from repository.items_repository import get_item, get_items_by_list, reduce_item_quantity, update_items_cache
from repository.favorites_repository import update_favorite_cache


async def get_orders_history(user_id):
    return await orders_repository.get_orders_history(user_id)


async def get_temp_order(user_id):
    return await orders_repository.get_temp_order(user_id)


async def add_item(user_id, item_id):
    item = await get_item(item_id)
    if item.stock > 0:
        return await orders_repository.add_item(user_id, item_id)
    else:
        return {"status": "failed", "message": "No stock available."}


async def remove_item(user_id, order_id, item_id):
    await orders_repository.remove_item(user_id, order_id, item_id)


async def confirm_order(user_id):
    temp_order = await get_temp_order(user_id)
    if temp_order is None:
        return {"status": "failed", "message": "Temp order invalid."}

    items_ids = []
    for item in temp_order.get('items'):
        items_ids.append(int(item['item_id']))

    items_in_database = await get_items_by_list(items_ids)
    for order_item in temp_order.get('items'):
        item_in_db = next((item for item in items_in_database if item.item_id == order_item["item_id"]), None)

        if not item_in_db:
            return {"status": "failed", "message": f"Item {order_item['item_id']} not found in stock."}

        if item_in_db.stock < order_item["quantity"]:
            return {
                "status": "failed",
                "message": f"Insufficient stock for item {order_item['name']} (available: {item_in_db.stock}, "
                           f"requested: {order_item['quantity']})."
            }

    for order_item in temp_order.get('items'):
        await reduce_item_quantity(order_item["item_id"], order_item["quantity"])

    await update_favorite_cache(user_id)
    await update_items_cache()

    return await orders_repository.confirm_order(temp_order)
