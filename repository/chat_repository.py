import json
from repository import cache_repository

CHAT_CACHE = "chat"
CHAT_PROMPT = ""


async def get_chat(user_id):
    cache_id = CHAT_CACHE + f"_{user_id}"
    if cache_repository.is_key_exists(cache_id):
        string_chat = cache_repository.get_cache_entity(cache_id)
        return json.loads(string_chat)
    else:
        return None


async def set_system(user_id):
    cache_id = CHAT_CACHE + f"_{user_id}"
    if not cache_repository.is_key_exists(cache_id):
        initial_input = [{"role": "system", "content": CHAT_PROMPT}]
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
