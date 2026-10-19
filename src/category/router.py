from src.user.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile

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
from src.user.model import UserRole


category_router = APIRouter(
    tags=["Categories"]
)

@category_router.get('/get/{category_id}', response_model=CategorySchemasBase)
async def get_category_by_id(category_id: int, session = Depends(get_db)):
    category = await CategoryService(session).get_category_by_id(category_id, is_active = True)
    return category


@category_router.get('/get/all/', response_model = list[CategorySchemasBase])
async def get_all_categories(skip: int=0, limit: int=100, session = Depends(get_db)):
    categories = await CategoryService(session).get_all_categories(skip, limit, is_active = True)
    return categories



@category_router.get('/get/name/{category_name}', response_model=CategorySchemasBase)
async def get_category_by_name(category_name: str, session = Depends(get_db)):
    category = await CategoryService(session).get_category_by_name(category_name, True)
    return category


@category_router.get("/image/{image_uuid}")
async def get_category_image(
    image_uuid: str,
    session = Depends(get_db) 
):
   res = await CategoryService(session).get_category_image(image_uuid)
   return res


@category_router.post("/create", response_model=CategoryCreateResponse)
async def create_new_category(
    category_data: CategoryCreateRequest,
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
    
    category = await CategoryService(session).create_new_category(category_data)
    return category


@category_router.patch("/update/{category_id}", response_model=CategoryUpdateResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdateRequest,
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
    
    category = await CategoryService(session).category_update(category_id, category_data)
    return category


@category_router.post("/image/{category_id}", status_code = status.HTTP_201_CREATED)
async def create_category_image(
    category_id: int,
    image: UploadFile,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    image_name = await CategoryService(session).create_category_image(category_id, current_user, image)
    return {
        "message": "Successfully created",
        "image name": f"{image_name}"
    }


@category_router.patch("/deactivate/{category_id}", response_model = CategoryDeactivateResponse)
async def category_deactivate(
    category_id: int, 
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
    
    res = await CategoryService(session).deactivate_category(category_id)
    return res


@category_router.get('/get/deactive/{category_id}', response_model=CategorySchemasBase)
async def get_deactive_category_by_id(
    category_id: int,
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
        
    category = await CategoryService(session).get_category_by_id(category_id, False)
    return category


@category_router.delete("/delete/{category_id}", response_model = CategoryDeleteResponse)
async def category_delete(
    category_id: int,
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
    
    res = await CategoryService(session).delete_category(category_id)
    return res