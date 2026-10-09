from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from src.dao.base import BaseDAO
from src.item.model import ItemModel
from src.item.schemas import ItemCreateSchemaDB, ItemResponseSchema
from sqlalchemy import select


class ItemDAO(BaseDAO[ItemModel, ItemCreateSchemaDB, ItemResponseSchema]):
    
    model = ItemModel
    
    async def get_items_by_price_range(self, min_price: Decimal, max_price: Decimal):
        result = await self.session.execute(
            select(self.model)
            .where(self.model.price.between(min_price,max_price))
        )
        return result.scalars().all()