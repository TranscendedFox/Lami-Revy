from fastapi import FastAPI
from controller.auth_controller import router as auth_router
from controller.user_controller import router as user_router
from controller.items_controller import router as items_router
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
