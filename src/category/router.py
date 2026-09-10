from fastapi import APIRouter

from src.category.schemas import(
    CategorySchemasBase,
    CategoryCreateRequest,
    CategoryCreateResponse,
    CategoryUpdateRequest,
    CategoryUpdateResponse
)
from src.category.service import CategoryService


category_router = APIRouter(
    tags=["Categories"]
)

categoryService = CategoryService()


@category_router.post("/create", response_model=CategoryCreateResponse)
async def create_new_category(category_data: CategoryCreateRequest):
    category = await categoryService.create_new_category(category_data)
    return category


@category_router.get('/get/all/')
async def get_all_categories(skip: int=0, limit: int=100):
    categories = await categoryService.get_all_categories(skip, limit)
    return categories


@category_router.get('/get/{category_id}', response_model=CategorySchemasBase)
async def get_category_by_id(category_id: int):
    category = await categoryService.get_category_by_id(category_id)
    return category


@category_router.patch("/update/{category_id}", response_model=CategoryUpdateResponse)
async def update_user(category_id: int, category_data: CategoryUpdateRequest):
    category = await categoryService.category_update(category_id, category_data)
    return category