from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Sequence

from src.category.model import CategoryModel
from src.dao.base import BaseDAO
from src.category.schemas import (
    CategoryCreateRequest,
    CategoryUpdateRequest
    )


class CategoryDAO(BaseDAO[CategoryModel, CategoryCreateRequest, CategoryUpdateRequest]):
    
    model = CategoryModel

    async def get_category_by_name(
        self,
        category_name: str,
        is_active: bool | None= True
    ) -> CategoryModel | None: 
        query = select(CategoryModel).where(CategoryModel.name==category_name)
        
        if is_active is not None:
            query = query.where(CategoryModel.is_active==is_active)
                        
        res = await self.session.execute(query)
        return res.scalar_one_or_none()
