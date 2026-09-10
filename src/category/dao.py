from sqlalchemy import select
from src.database import AsyncSessionLocal, get_db
from src.category.model import CategoryModel


class CategoryDAO:
    
    def __init__(self, database):
        self.database = database

    
    async def get_all_categories(self, skip: int=0, limit: int=100) -> CategoryModel | None:
            async with AsyncSessionLocal() as session:
                res = await session.execute(
                    select(CategoryModel).offset(skip).limit(limit)
                )
                return res.scalars().all()

    
    async def get_category_by_id(self, category_id: int) -> CategoryModel | None:
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(CategoryModel).where(CategoryModel.id==category_id))
            return res.scalar_one_or_none()

    
    async def get_category_by_name(self, category_name: str) -> CategoryModel | None:
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(CategoryModel).where(CategoryModel.name==category_name))
            return res.scalar_one_or_none()

    
    async def create_new_catetory(self, category_data_dict: dict) -> CategoryModel:
        async with AsyncSessionLocal() as session:
            category = CategoryModel(**category_data_dict)
            session.add(category)
            await session.commit()
            await session.refresh(category)
            return category
    
    
    async def update_catetory(self, catetory_id:int, catetory_data_dict: dict) -> CategoryModel:
        async with AsyncSessionLocal() as session:
            db_category = await session.get(CategoryModel, catetory_id)
            
            if not db_category:
                return None
            
            for key, value in catetory_data_dict.items():
                setattr(db_category, key, value)
            
            await session.commit()
            await session.refresh(db_category)
            return db_category
