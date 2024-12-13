from fastapi.security import OAuth2PasswordBearer
from starlette import status
from fastapi import APIRouter, Depends
from service import orders_service
from service import auth_service
from exceptions.security_exceptions import token_exception

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={401: {"orders": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_orders(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()

    orders_history = await orders_service.get_orders_history(user_response.id)
    temp_order = await orders_service.get_temp_order(user_response.id)

    return {
        "temp_order": temp_order,
        "orders_history": orders_history
    }


@router.post("/{item_id}", status_code=status.HTTP_201_CREATED)
async def add_item(item_id, token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    else:
        await orders_service.add_item(user_response.id, item_id)


@router.delete("/{order_id}/{item_id}", status_code=status.HTTP_201_CREATED)
async def remove_item(item_id, order_id, token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    else:
        await orders_service.remove_item(user_response.id, order_id, item_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def confirm_order(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    else:
        return await orders_service.confirm_order(user_response.id)
