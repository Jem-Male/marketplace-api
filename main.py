from src.database import Base, engine
from fastapi import FastAPI
from typing import Annotated
from src.user.router import user_router
from src.category.router import category_router
from src.store.router import store_router
from src.item.router import item_router

app = FastAPI()


@app.get("/")
async def welcome_msg():
    return {"message": "Hello World"}


app.include_router(user_router, prefix='/user')
# app.include_router(category_router, prefix='/category')
# app.include_router(store_router, prefix='/store')
# app.include_router(item_router, prefix='/item')