from fastapi.security import OAuth2PasswordBearer
from starlette import status
from fastapi import APIRouter, Depends
from service import favorites_service
from service import auth_service
from exceptions.security_exceptions import token_exception

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"],
    responses={401: {"favorites": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_favorites(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    return await favorites_service.get_favorites(user_response.id)


@router.post("/{item_id}", status_code=status.HTTP_201_CREATED)
async def add_favorite(item_id, token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    else:
        await favorites_service.add_favorite(user_response.id, item_id)


@router.delete("/{item_id}", status_code=status.HTTP_201_CREATED)
async def remove_favorite(item_id, token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    else:
        await favorites_service.remove_favorite(user_response.id, item_id)
