from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status,
    UploadFile
) 

from src.store.schemas import(
    StoreSchemasBase,
    StoreCreateRequest,
    StoreCreateResponse,
    StoreDeactivateResponse,
    StoreUpdateResponse,
    StoreUpdateRequest,
    StoreDeleteResponse
)
from src.store.service import StoreService
from src.database import get_db
from src.user.auth import get_current_user
from src.user.model import UserRole


store_router = APIRouter(
    tags=["Store"]
)


@store_router.post("/create", response_model=StoreCreateResponse)
async def create_store(
    store_data: StoreCreateRequest, 
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    store = await StoreService(session).create_store(store_data, current_user)
    return store


@store_router.get('/get/all/')
async def get_all_stores(skip: int=0, limit: int=100, session = Depends(get_db)):
    stores = await StoreService(session).get_all_stores(skip, limit)
    return stores


@store_router.get("/image/{image_uuid}")
async def get_store_image(
    image_uuid: str,
    session = Depends(get_db) 
):
   res = await StoreService(session).get_store_image(image_uuid)
   return res



@store_router.get('/get/{store_id}', response_model=StoreSchemasBase)
async def get_store_by_id(store_id: int, session = Depends(get_db)):
    store = await StoreService(session).get_store_by_id(store_id, True)
    return store


@store_router.patch("/update/{store_id}", response_model=StoreUpdateResponse)
async def update_store(
    store_id: int,
    store_data: StoreUpdateRequest,
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    store = await StoreService(session).update_store(store_id, store_data, current_user)
    return store


@store_router.post("/image/{store_id}", status_code = status.HTTP_201_CREATED)
async def create_store_image(
    store_id: int,
    image: UploadFile,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    image_name = await StoreService(session).create_store_image(store_id, current_user, image)
    return {
        "message": "Successfully created",
        "image name": f"{image_name}"
    }


@store_router.patch("/deactivate/{store_id}", response_model=StoreDeactivateResponse)
async def deactivate_store(
    store_id: int, 
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    res = await StoreService(session).deactivate_store(store_id, current_user)
    return res


@store_router.get('/get/deactive/{store_id}', response_model=StoreSchemasBase)
async def get_deactivated_store_by_id(store_id: int, session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user["role"] != UserRole.ADMIN.value:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "No editing rights"   
        )
    store = await StoreService(session).get_store_by_id(store_id, False)
    return store


@store_router.delete("/delete/{store_id}", response_model=StoreDeleteResponse)
async def delete_store(store_id: int, session = Depends(get_db), current_user = Depends(get_current_user)):
    res = await StoreService(session).delete_store(store_id, current_user)
    return res