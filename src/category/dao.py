from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.database import AsyncSessionLocal, get_db
from src.category.model import CategoryModel


class CategoryDAO:
    
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def get_all_categories(self, skip: int=0, limit: int=100) -> CategoryModel | None:
            res = await self.session.execute(
                select(CategoryModel).offset(skip).limit(limit)
            )
            return res.scalars().all()

    
    async def get_category_by_id(self, category_id: int) -> CategoryModel | None:
        res = await self.session.execute(select(CategoryModel).where(CategoryModel.id==category_id))
        return res.scalar_one_or_none()

    
    async def get_category_by_name(self, category_name: str) -> CategoryModel | None:
        res = await self.session.execute(select(CategoryModel).where(CategoryModel.name==category_name))
        return res.scalar_one_or_none()

    
    async def create_new_catetory(self, category_data_dict: dict) -> CategoryModel:
        category = CategoryModel(**category_data_dict)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category
    
    
    async def update_catetory(self, catetory_id:int, catetory_data_dict: dict) -> CategoryModel:        
        db_category = await self.session.get(CategoryModel, catetory_id)
        
        if not db_category:
            return None
        
        for key, value in catetory_data_dict.items():
            setattr(db_category, key, value)
        
        await self.session.commit()
        await self.session.refresh(db_category)
        return db_category

    
    async def delete_category(self, category_id: int) -> CategoryModel:
        res = await self.session.execute(delete(CategoryModel).where(CategoryModel.id==category_id))
        await self.session.commit()
        return res.rowcount > 0