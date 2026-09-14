from fastapi import APIRouter, Depends

from src.category.schemas import(
    CategorySchemasBase,
    CategoryCreateRequest,
    CategoryCreateResponse,
    CategoryUpdateRequest,
    CategoryUpdateResponse
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
    category = await CategoryService(session).get_category_by_id(category_id)
    return category


@category_router.patch("/update/{category_id}", response_model=CategoryUpdateResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdateRequest,
    session = Depends(get_db)
):
    category = await CategoryService(session).category_update(category_id, category_data)
    return category


@category_router.patch("/deactivate/{category_id}", response_model=)
async def category_deactivate(
    catrgory_id: int, 
    session = Depends(get_db)
):
    res = await CategoryService(session).deactivate_category(catrgory_id)
    return res


@user_router.delete("/delete/{user_id}", response_model=UserDeleteResponse)
async def user_delete(
    user_id: int, 
    user_data: UserDeleteRequest,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    userService = UserService(session)
    res = await userService.delete_user(user_id, user_data)
    return res


@user_router.get('/deactive/{user_id}', response_model=UserResponseSchemas)
async def get_deactive_user(
    user_id: int,
    session = Depends(get_db)
):
    userService = UserService(session)
    res = await userService.get_deactive_user_by_id(user_id)
    return res