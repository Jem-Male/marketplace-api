from src.database import Base, engine
from fastapi import FastAPI
from typing import Annotated
from src.user.router import user_router
from src.category.router import category_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_router, prefix='/user')
app.include_router(category_router, prefix='/category')