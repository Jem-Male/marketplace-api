from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.item.dao import ItemDAO
from src.item.schemas import ItemCreateSchema, ItemUpdaiteSchema, ItemResponseSchema
from src.item.model import ItemModel


class ItemService:
    @classmethod
    async def create_new_item(
        cls, session: AsyncSession, item_data: ItemCreateSchema, user_id: int
    ) -> ItemModel:

        user_items = await ItemDAO.get_items_by_owner(session, owner_id=user_id)
                    
        full_data = item_data.model_dump()
        full_data["owner_id"] = user_id
        
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