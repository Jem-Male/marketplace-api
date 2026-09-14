from pydantic import TypeAdapter
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.schemas import(
    CategorySchemasBase,
    CategoryCreateRequest,
    CategoryCreateResponse,
    CategoryUpdateRequest,
    CategoryUpdateResponse,
    CategoryDeactivateResponse,
    CategoryDeleteResponse
)
from src.category.dao import CategoryDAO
from src.category.model import CategoryModel


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.category_dao = CategoryDAO(session)
    
    async def get_all_categories(self, skip: int, limit: int) -> list[CategorySchemasBase]:    
        if skip < 0 or limit <= 0 or limit < skip:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bad query"
            )
        
        categories = await self.category_dao.get_all_categories(skip, limit)
                
        return TypeAdapter(list[CategorySchemasBase]).validate_python(categories)


    async def get_category_by_id(self, category_id: int) -> CategorySchemasBase:
        category = await self.category_dao.get_category_by_id(category_id)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is not found"
            )
        
        return CategorySchemasBase.model_validate(category)


    async def get_category_by_name(self, category_name: str) -> CategorySchemasBase:
        category = await self.category_dao.get_category_by_name(category_name)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is not found"
            )
                
        return CategorySchemasBase.model_validate(category)


    async def create_new_category(self, category_data: CategoryCreateRequest) -> CategoryCreateResponse:
        category_exist = await self.category_dao.get_category_by_name(category_data.name)
        if category_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is exits"
            )
        
        dict_category_data = category_data.model_dump()
        
        created_category = await self.category_dao.create_new_catetory(dict_category_data)
        
        return CategoryCreateResponse.model_validate(created_category)


    async def category_update(self, category_id: int, category_data: CategoryUpdateRequest) -> CategoryUpdateResponse:
        category = await self.category_dao.get_category_by_id(category_id)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="category in not found"
            )
        
        update_data = category_data.model_dump(exclude_unset=True)
        
        if "name" in category_data:
            exiting_category = await self.category_dao.get_category_by_name(update_data["name"])
            if exiting_category and exiting_category.id != category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="category already registered"
                )
        
        updated_data = await self.category_dao.update_catetory(category_id, update_data)
        
        return CategoryUpdateResponse.model_validate(updated_data)
        
    
    async def deactivate_category(self, category_id: int) -> CategoryDeactivateResponse:
        category = await self.category_dao.get_category_by_id(category_id)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="category in not found"
            )
        
        return CategoryDeactivateResponse.model_validate(category)
    
    
    async def delete_category(self, category_id: int, ) -> CategoryDeleteResponse:
            db_category = await self.user_dao.get_deactive_category_by_id(category_id)
            
            if db_category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="category in not found"
                )
                        
            res = await self.category_dao.delete_category(category_id)
            
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="fatal delet"
                )
            
            return CategoryDeleteResponse.model_validate(res)