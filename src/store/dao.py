from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Sequence

from src.store.model import StoreModel


class StoreDAO:
    
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_stores(
        self, 
        skip: int=0, 
        limit: int=100, 
        category_status: bool | None = True
    ) -> Sequence[StoreModel] | None:
        
        query = select(StoreModel)
        
        if category_status is not None:
            query = query.where(StoreModel.is_active==category_status)
        
        query = query.offset(skip).limit(limit)
        
        res = await self.session.execute(query)
        return res.scalars().all()

    
    async def get_store_by_id(
        self,
        category_id: int,
        category_status: bool | None = True
    ) -> StoreModel | None:
        
        query = select(StoreModel).where(StoreModel.id==category_id)
        
        if category_status is not None:
            query = query.where(StoreModel.is_active==category_status)
        
        res = await self.session.execute(query)
        return res.scalar_one_or_none()


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


    async def create_new_store(self, category_data_dict: dict) -> StoreModel:
        category = StoreModel(**category_data_dict)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category
    
    
    async def update_store(self, category: StoreModel) -> StoreModel:
        await self.session.commit()
        await self.session.refresh(category)
        return category


    async def delete_store(self, category_id: int) -> bool:
        res = await self.session.execute(delete(StoreModel).where(StoreModel.id==category_id))
        await self.session.commit()
        return res.rowcount > 0
    
    
    async def deactivate_store(self, category_id: int) -> bool:
        res = await self.session.execute(
            update(StoreModel)
            .where(StoreModel.id == category_id)
            .values(is_active=False)
        )
        await self.session.commit()
        return res.rowcount > 0