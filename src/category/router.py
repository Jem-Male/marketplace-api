from fastapi import APIRouter, Depends

from src.category.schemas import(
    CategorySchemasBase,
    CategoryCreateRequest,
    CategoryCreateResponse,
    CategoryUpdateRequest,
    CategoryUpdateResponse,
    CategoryDeactivateResponse,
    CategoryDeleteResponse
)
from src.category.service import CategoryService
from src.database import get_db

category_router = APIRouter(
    tags=["Categories"]
)


@category_router.post("/create", response_model=CategoryCreateResponse)
async def create_new_category(category_data: CategoryCreateRequest, session = Depends(get_db)):
    category = await CategoryService(session).create_new_category(category_data)
    return category


@category_router.get('/get/all/')
async def get_all_categories(skip: int=0, limit: int=100, session = Depends(get_db)):
    categories = await CategoryService(session).get_all_categories(skip, limit)
    return categories


@category_router.get('/get/{category_id}', response_model=CategorySchemasBase)
async def get_category_by_id(category_id: int, session = Depends(get_db)):
    category = await CategoryService(session).get_category_by_id(category_id, True)
    return category


@category_router.get('/get/name/{category_name}', response_model=CategorySchemasBase)
async def get_category_by_name(category_name: str, session = Depends(get_db)):
    category = await CategoryService(session).get_category_by_name(category_name, True)
    return category


@category_router.patch("/update/{category_id}", response_model=CategoryUpdateResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdateRequest,
    session = Depends(get_db)
):
    category = await CategoryService(session).category_update(category_id, category_data)
    return category


@category_router.patch("/deactivate/{category_id}", response_model = CategoryDeactivateResponse)
async def category_deactivate(
    catrgory_id: int, 
    session = Depends(get_db)
):
    res = await CategoryService(session).deactivate_category(catrgory_id)
    return res


@category_router.get('/get/deactive/{category_id}', response_model=CategorySchemasBase)
async def get_deactive_category_by_id(category_id: int, session = Depends(get_db)):
    category = await CategoryService(session).get_category_by_id(category_id, False)
    return category


@category_router.delete("/delete/{category_id}", response_model = CategoryDeleteResponse)
async def category_delete(category_id: int, session = Depends(get_db)):
    res = await CategoryService(session).delete_category(category_id)
    return res