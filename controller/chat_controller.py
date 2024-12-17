from fastapi.security import OAuth2PasswordBearer
from starlette import status
from fastapi import APIRouter, Depends
from service import auth_service
from service import chat_service
from exceptions.security_exceptions import token_exception
from model.message_request import MessageRequest

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={401: {"chat": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_chat(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    return await chat_service.get_chat(user_response.id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def set_message(request: MessageRequest, token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()

    await chat_service.set_message(user_response.id, request.message)


@router.delete("/", status_code=status.HTTP_201_CREATED)
async def reset_chat(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()

    await chat_service.reset_chat(user_response.id)
