from pydantic import TypeAdapter
from fastapi import UploadFile
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
from src.file.file import File
from src.category.dao import CategoryDAO
from src.category.exceptions import (
    CategoryErrors as CategoryEr,
    QueruErrors as QueruEr,
    DBErrors as DBEr
) 
from src.user.model import UserRole

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.category_dao = CategoryDAO(session)


    async def get_all_categories(self, skip: int, limit: int, is_active: bool = True) -> list[CategorySchemasBase]:    
        if skip < 0 or limit <= 0 or limit < skip:
            raise QueruEr.bad_query()
        
        categories = await self.category_dao.get_all(skip, limit, is_active)
        return TypeAdapter(list[CategorySchemasBase]).validate_python(categories)

    
    async def get_category_by_id(self, category_id: int, is_active: bool = True) -> CategorySchemasBase:
        category = await self.category_dao.get_by_id(category_id, is_active)
        
        if category is None:
            raise CategoryEr.category_not_found()
        
        return CategorySchemasBase.model_validate(category)


    async def get_category_by_name(self, category_name: str, is_active: bool = True) -> CategorySchemasBase:
        category = await self.category_dao.get_category_by_name(category_name, is_active)
        
        if category is None:
            raise CategoryEr.category_not_found()
                
        return CategorySchemasBase.model_validate(category)


    async def create_new_category(self, category_data: CategoryCreateRequest) -> CategoryCreateResponse:
        
        category_exist = await self.category_dao.get_category_by_name(category_data.name, True)
        if category_exist is not None:
            raise CategoryEr.category_is_exists()
        
        created_category = await self.category_dao.create(category_data)
        
        return CategoryCreateResponse.model_validate(created_category)

    
    async def create_category_image(self, category_id: int, image: UploadFile) -> str:
        category = await self.get_category_by_id(category_id, is_active=True)
        
        uuid = await File.create_image(image, category.image)
        category.image = uuid
        valid_image = CategoryUpdateRequest(image = uuid)
        await self.category_dao.update(record_id=category_id, schema=valid_image)
        return uuid
    
    
    async def get_category_image(self, image_uuid):
        image = await File.get_image(image_uuid)
        return image
    

    async def category_update(self, category_id: int, category_data: CategoryUpdateRequest) -> CategoryUpdateResponse:
        await self.get_category_by_id(category_id, True)
        
        if category_data.name:
            exiting_category = await self.category_dao.get_category_by_name(category_data.name, True)
            if exiting_category and exiting_category.id != category_id:
                raise CategoryEr.category_is_exists()
        
        updated_data = await self.category_dao.update(category_id ,category_data)
        
        return CategoryUpdateResponse.model_validate(updated_data)
        
    
    async def deactivate_category(self, category_id: int) -> CategoryDeactivateResponse:
        category = await self.get_category_by_id(category_id, True)
        
        category.is_active = False
        
        res = await self.category_dao.update(category_id, category)

        if not res:
            raise DBEr.fatal_deactivaite()
        
        return CategoryDeactivateResponse(id=category_id)


    async def delete_category(self, category_id: int) -> CategoryDeleteResponse:
            await self.get_category_by_id(category_id, None)

            res = await self.category_dao.delete(category_id)
            
            if not res:
                raise DBEr.fatal_delet()
            
            return CategoryDeleteResponse(id = category_id)