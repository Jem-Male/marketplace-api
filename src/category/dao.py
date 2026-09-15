from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Sequence

from src.category.model import CategoryModel


class CategoryDAO:
    
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_categories(
        self, 
        skip: int=0, 
        limit: int=100, 
        category_status: bool | None = True
    ) -> Sequence[CategoryModel] | None:
        
        query = select(CategoryModel)
        
        if category_status is not None:
            query = query.where(CategoryModel.is_active==category_status)
        
        query = query.offset(skip).limit(limit)
        
        res = await self.session.execute(query)
        return res.scalars().all()

    
    async def get_category_by_id(
        self,
        category_id: int,
        category_status: bool | None = True
    ) -> CategoryModel | None:
        
        query = select(CategoryModel).where(CategoryModel.id==category_id)
        
        if category_status is not None:
            query = query.where(CategoryModel.is_active==category_status)
        
        res = await self.session.execute(query)
        return res.scalar_one_or_none()


    async def get_category_by_name(
        self,
        category_name: str,
        category_status: bool | None= True
    ) -> CategoryModel | None: 
        query = select(CategoryModel).where(CategoryModel.name==category_name)
        
        if category_status is not None:
            query = query.where(CategoryModel.is_active==category_status)
                        
        res = await self.session.execute(query)
        return res.scalar_one_or_none()


    async def create_new_catetory(self, category_data_dict: dict) -> CategoryModel:
        category = CategoryModel(**category_data_dict)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category
    
    
    async def update_category(self, category: CategoryModel) -> CategoryModel:
        await self.session.commit()
        await self.session.refresh(category)
        return category


    async def delete_category(self, category_id: int) -> bool:
        res = await self.session.execute(delete(CategoryModel).where(CategoryModel.id==category_id))
        await self.session.commit()
        return res.rowcount > 0
    
    
    async def deactivate_category(self, category_id: int) -> bool:
        res = await self.session.execute(
            update(CategoryModel)
            .where(CategoryModel.id == category_id)
            .values(is_active=False)
        )
        await self.session.commit()
        return res.rowcount > 0