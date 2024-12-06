from starlette import status
from fastapi import APIRouter
from service import items_service

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={401: {"items": "Not authorized"}}
)


@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_all_items():
    return await items_service.get_all_items()


@router.get("/search/{search}", status_code=status.HTTP_201_CREATED)
async def get_items_by_search(search: str):
    return await items_service.get_items_by_search(search)
