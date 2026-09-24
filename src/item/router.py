from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import APIRouter, status, Depends

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
    prefix="/items",
    tags=["Items"]
)

@item_router.get(
    "/all",
    response_model=List[ItemBaseSchema],
    summary = "get list items"
)
async def get_all(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    return await ItemService.get_all_items(session, skip, limit)


@item_router.post(
    "/create",
    response_model=ItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item"
)
async def create_item(
    item_data: ItemCreateSchema,
    session: AsyncSession = Depends(get_db),
    current_user_id = Depends(get_current_user)
):
    return await ItemService.create_new_item(
        session,
        item_data,
        current_user_id
    )


@item_router.get(
    '/{item_id}',
    response_model=ItemResponseSchema,
    summary="Get item by id"
)
async def get_current_item(
    item_id: int,
    session: AsyncSession = Depends(get_db)
):
    return await ItemService.get_item_safely(session, item_id)


@item_router.put(
    "/{item_id}", 
    response_model=ItemResponseSchema,
    summary="Update item"
)
async def update_item(
    item_id: int,
    item_data: ItemUpdaiteSchema,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return await ItemService.update_item_safely(session, item_id, item_data, current_user_id)


@item_router.delete(
    "/{item_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delet item"
)
async def delete_item(
    item_id: int,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    await ItemService.delete_item_safely(session, item_id, current_user_id)
    return None