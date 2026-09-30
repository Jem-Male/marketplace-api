from dns.update import Update
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.item.dao import ItemDAO
from src.user.dao import UserDAO
from src.category.dao import CategoryDAO
from src.store.dao import StoreDAO
from src.item.schemas import (
    ItemCreateSchema,
    ItemUpdaiteSchema, 
    ItemResponseSchema,
    ItemCreateSchemaDB
)
from src.item.model import ItemModel


class ItemService:
    @classmethod
    async def create_new_item(
        cls, session: AsyncSession, item_data: ItemCreateSchema, user_id: int
    ) -> ItemModel:
        active_user = await UserDAO(session).get_active_user_by_id(user_id)
        if not active_user:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'User not found'
            )

        active_category = await CategoryDAO(session).get_category_by_id(item_data.category)
        if not active_category:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'Category not found'
            )

        active_store = await StoreDAO.get_by_id(session, item_data.store)
        if not active_store:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'Store not found'
            )
        
        item_data = ItemCreateSchemaDB(**item_data.model_dump(), creator=user_id)
        return await ItemDAO.create(session, item_data)


    @classmethod
    async def get_item_safely(cls, session: AsyncSession, item_id: int) -> ItemModel:
        item = await ItemDAO.get_by_id(session, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с ID {item_id} не найден."
            )
        return item
    
    
    @classmethod
    async def get_all_items(
        cls, session: AsyncSession, skip: int, limit: int, is_active: bool
    ) -> ItemModel:
        if limit < 0 or skip < 0 or limit < skip:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "Bad request"
            ) 
        return await ItemDAO.get_all(session, skip, limit, is_active)
    
    
    @classmethod
    async def update_item_safely(
        cls, session: AsyncSession, item_id: int, item_data: ItemUpdaiteSchema, user_id: int
    ) -> ItemModel:
        item = await ItemDAO.get_by_id(session, item_id)
        
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is not found"
            )
        try:
            if item.creator != user_id:
                raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail = "No editing rights"
                )
        except:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Err"
            )
        
        return await ItemDAO.update(session, item_id, item_data)
    
    
    @classmethod
    async def delete_item_safely(
        cls, session: AsyncSession, item_id: int, user_id: int
    ) -> bool:
        item = await ItemDAO.get_by_id(session, item_id)
                
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is not found"
            )
        
        if item.creator != user_id:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "No editing rights"
            )
        
        return await ItemDAO.delete(session, item_id)