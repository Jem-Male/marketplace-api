from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Sequence

from src.store.model import StoreModel
from src.dao.base import BaseDAO
from src.store.schemas import(
    StoreSchemasBase,
    StoreCreateRequest,
    StoreCreateResponse,
    StoreDeactivateResponse,
    StoreUpdateResponse,
    StoreUpdateRequest,
    StoreDeleteResponse
)

class StoreDAO(BaseDAO[StoreModel, StoreCreateRequest, StoreUpdateRequest]):
    
    model = StoreModel

    async def get_store_by_name(
        self,
        category_name: str,
        category_status: bool | None = True
    ) -> StoreModel | None: 
        query = select(StoreModel).where(StoreModel.name==category_name)
        
        if category_status is not None:
            query = query.where(StoreModel.is_active==category_status)

        res = await self.session.execute(query)
        return res.scalar_one_or_none()
