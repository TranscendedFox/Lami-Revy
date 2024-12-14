from repository import favorites_repository


async def get_favorites(user_id):
    return await favorites_repository.get_favorites(user_id)


async def add_favorite(user_id, item_id):
    return await favorites_repository.add_favorite(user_id, item_id)


async def remove_favorite(user_id, item_id):
    await favorites_repository.remove_favorite(user_id, item_id)