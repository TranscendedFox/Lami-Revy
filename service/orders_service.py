from repository import orders_repository


async def get_orders_history(user_id):
    return await orders_repository.get_orders_history(user_id)


async def get_temp_order(user_id):
    return await orders_repository.get_temp_order(user_id)


async def add_item(user_id, item_id):
    await orders_repository.add_item(user_id, item_id)


async def remove_item(order_id, item_id):
    await orders_repository.remove_item(order_id, item_id)


async def confirm_order(user_id):
    await orders_repository.confirm_order(user_id)
