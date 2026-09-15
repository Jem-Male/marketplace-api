from fastapi import APIRouter, Depends

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

store_router = APIRouter(
    tags=["Store"]
)


@store_router.post("/create", response_model=StoreCreateResponse)
async def create_store(store_data: StoreCreateRequest, session = Depends(get_db)):
    store = await StoreService(session).create_store(store_data)
    return store


@store_router.get('/get/all/')
async def get_all_stores(skip: int=0, limit: int=100, session = Depends(get_db)):
    stores = await StoreService(session).get_all_stores(skip, limit)
    return stores


@store_router.get('/get/{store_id}', response_model=StoreSchemasBase)
async def get_store_by_id(store_id: int, session = Depends(get_db)):
    store = await StoreService(session).get_store_by_id(store_id, True)
    return store


@store_router.patch("/update/{store_id}", response_model=StoreUpdateResponse)
async def update_store(
    store_id: int,
    store_data: StoreUpdateRequest,
    session = Depends(get_db)
):
    store = await StoreService(session).update_store(store_id, store_data)
    return store


@store_router.patch("/deactivate/{store_id}", response_model=StoreDeactivateResponse)
async def deactivate_store(
    store_id: int, 
    session = Depends(get_db)
):
    res = await StoreService(session).deactivate_store(store_id)
    return res


@store_router.get('/get/deactive/{store_id}', response_model=StoreSchemasBase)
async def get_deactivated_store_by_id(store_id: int, session = Depends(get_db)):
    store = await StoreService(session).get_store_by_id(store_id, False)
    return store


@store_router.delete("/delete/{store_id}", response_model=StoreDeleteResponse)
async def delete_store(store_id: int, session = Depends(get_db)):
    res = await StoreService(session).delete_store(store_id)
    return res