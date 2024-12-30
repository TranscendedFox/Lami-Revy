from fastapi import FastAPI
from controller.auth_controller import router as auth_router
from controller.user_controller import router as user_router
from controller.items_controller import router as items_router
from controller.favorites_controller import router as favorites_router
from controller.orders_controller import router as orders_router
from controller.chat_controller import router as chat_router
from analytics.api.analytics_api import router as analytics_router
from repository.database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(items_router)
app.include_router(favorites_router)
app.include_router(orders_router)
app.include_router(chat_router)
app.include_router(analytics_router)
