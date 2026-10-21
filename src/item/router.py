from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import APIRouter, status, Depends, UploadFile

from src.database import get_db
from src.item.service import ItemService
from src.user.auth import get_current_user
from src.item.schemas import (
    ItemBaseSchema,
    ItemCreateSchema,
    ItemResponseSchema,
    ItemUpdaiteSchema    
)


item_router = APIRouter(
    tags=["Items"]
)

@item_router.get(
    "/all",
    response_model=List[ItemResponseSchema],
    summary = "get list items"
)
async def get_all(
    skip: int = 0,
    limit: int = 10000,
    session: AsyncSession = Depends(get_db)
):
    return await ItemService(session).get_all_items(skip, limit, True)


@item_router.post(
    "/create",
    response_model=ItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item"
)
async def create_item(
    item_data: ItemCreateSchema,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await ItemService(session).create_new_item(item_data, current_user)


@item_router.get("/image/{image_uuid}")
async def get_item_image(
    image_uuid: str,
    session = Depends(get_db) 
):
   res = await ItemService(session).get_item_image(image_uuid)
   return res


@item_router.get(
    '/{item_id}',
    response_model=ItemResponseSchema,
    summary="Get item by id"
)
async def get_current_item(
    item_id: int,
    session: AsyncSession = Depends(get_db)
):
    return await ItemService(session).get_item_safely(item_id)


@item_router.put(
    "/{item_id}", 
    response_model=ItemResponseSchema,
    summary="Update item"
)
async def update_item(
    item_id: int,
    item_data: ItemUpdaiteSchema,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await ItemService(session).update_item_safely(item_id, item_data, current_user)


@item_router.post("/image/{item_id}", status_code = status.HTTP_201_CREATED)
async def create_item_image(
    item_id: int,
    file: UploadFile,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    image_name = await ItemService(session).create_item_image(item_id, current_user, file)
    return {
        "message": "Successfully created",
        "image name": f"{image_name}"
    }


@item_router.delete(
    "/{item_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delet item"
)
async def delete_item(
    item_id: int,
    session: AsyncSession = Depends(get_db),
    current_user= Depends(get_current_user)
):
    await ItemService(session).delete_item_safely(item_id, current_user)
    return None