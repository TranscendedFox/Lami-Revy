from repository import chat_repository
from service.items_service import get_all_items
from openAIClient.openai_client import get_response


async def get_chat(user_id):
    return await chat_repository.get_chat(user_id)


async def set_message(user_id, message):
    chat = await get_chat(user_id)

    if chat is not None:
        user_message_count = sum(1 for msg in chat if msg.get('role') == 'user')

        if user_message_count >= 5:
            return {"error": "User has already sent 5 or more messages."}

    else:
        await chat_repository.set_system(user_id, await get_all_items())

    await chat_repository.set_message(user_id, message, "user")

    openai_response = get_response(await get_chat(user_id))
    await chat_repository.set_message(user_id, openai_response, "assistant")


async def reset_chat(user_id):
    return await chat_repository.reset_chat(user_id)
