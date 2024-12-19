import json
from repository import cache_repository

CHAT_CACHE = "chat"
CHAT_PROMPT = """
You are a shopping assistant for an e-commerce website 'Lamy-Revi'. Your job is to:
- Provide detailed and accurate information about products available in the store.
- Indicate if a product is in stock or out of stock when asked.
- Be concise, polite, and helpful.

You have access to product information such as name, price, description, and stock status. If a user asks about an unavailable product, apologize and suggest alternatives.
"""


async def get_chat(user_id):
    cache_id = CHAT_CACHE + f"_{user_id}"
    if cache_repository.is_key_exists(cache_id):
        string_chat = cache_repository.get_cache_entity(cache_id)
        return json.loads(string_chat)
    else:
        return None


async def set_system(user_id, items):
    cache_id = CHAT_CACHE + f"_{user_id}"
    items_dict = [item.dict() for item in items]
    if not cache_repository.is_key_exists(cache_id):
        initial_input = [{"role": "system", "content": CHAT_PROMPT},
                         {"role": "system", "content": json.dumps(items_dict)}]
        cache_repository.update_cache_entity(cache_id, json.dumps(initial_input))


async def set_message(user_id, message, role):
    cache_id = CHAT_CACHE + f"_{user_id}"
    chat = await get_chat(user_id)

    if chat is not None:
        chat.append({"role": role, "content": message})
        cache_repository.update_cache_entity(cache_id, json.dumps(chat))


async def reset_chat(user_id):
    cache_id = CHAT_CACHE + f"_{user_id}"

    if cache_repository.is_key_exists(cache_id):
        cache_repository.remove_cache_entity(cache_id)
