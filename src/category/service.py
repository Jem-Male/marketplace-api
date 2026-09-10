from pydantic import TypeAdapter
from fastapi import HTTPException, status

from src.category.schemas import(
    CategorySchemasBase,
    CategoryCreateRequest,
    CategoryCreateResponse,
    CategoryUpdateRequest,
    CategoryUpdateResponse
)
from src.category.dao import CategoryDAO
from src.category.model import CategoryModel


categoryDAO = CategoryDAO(CategoryModel)


class CategoryService:
    
    async def get_all_categories(self, skip: int, limit: int) -> list[CategorySchemasBase]:
    
        if skip < 0 or limit <= 0 or limit < skip:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bad query"
            )
        
        categories = await categoryDAO.get_all_categories(skip, limit)
                
        return TypeAdapter(list[CategorySchemasBase]).validate_python(categories)


    async def get_category_by_id(self, category_id: int) -> CategorySchemasBase:
        category = await categoryDAO.get_category_by_id(category_id)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is not found"
            )
        
        # return CategorySchemasBase(
        #     id=category.id,
        #     name=category.name,
        #     description=category.description,
        #     image=category.image,
        #     created_at=category.created_at,
        #     updated_at=category.updated_at,
        #     is_active=category.is_active
        # )
        
        return CategorySchemasBase.model_validate(category)
    
    
    async def get_category_by_name(self, category_name: str) -> CategorySchemasBase:
        category = await categoryDAO.get_category_by_name(category_name)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is not found"
            )
        
        # return CategorySchemasBase(
        #     id=category.id,
        #     name=category.name,
        #     description=category.description,
        #     image=category.image,
        #     created_at=category.created_at,
        #     updated_at=category.updated_at,
        #     is_active=category.is_active
        # )
        
        return CategorySchemasBase.model_validate(category)
    
    
    async def create_new_category(self, category_data: CategoryCreateRequest) -> CategoryCreateResponse:
        category_exist = await categoryDAO.get_category_by_name(category_data.name)
        if category_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category is exits"
            )
        
        dict_category_data = category_data.model_dump()
        
        created_category = await categoryDAO.create_new_catetory(dict_category_data)
        
        return CategoryCreateResponse(id=created_category.id)

    
    async def category_update(self, category_id: int, category_data: CategoryUpdateRequest) -> CategoryUpdateResponse:
        category = await categoryDAO.get_category_by_id(category_id)
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="category in not found"
            )
        
        update_data = category_data.model_dump(exclude_unset=True)
        
        if "name" in category_data:
            exiting_category = await categoryDAO.get_category_by_name(update_data["name"])
            if exiting_category and exiting_category.id != category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="category already registered"
                )
        
        updated_data = await categoryDAO.update_catetory(category_id, update_data)
        
        return CategoryUpdateResponse(
            id=updated_data.id
        )