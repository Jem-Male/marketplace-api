from pydantic import TypeAdapter
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.store.schemas import(
    StoreSchemasBase,
    StoreCreateRequest,
    StoreCreateResponse,
    StoreDeactivateResponse,
    StoreUpdateResponse,
    StoreUpdateRequest,
    StoreDeleteResponse
)
from src.store.dao import StoreDAO


class StoreService:
    def __init__(self, session: AsyncSession):
        self.store_dao = StoreDAO(session)


    async def get_all_stores(
        self,
        skip: int,
        limit: int,
        is_active: bool | None = None
    ) -> list[StoreSchemasBase]:
        if skip < 0 or limit <= 0 or limit < skip:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bad query"
            )

        stores = await self.store_dao.get_all(
            self.store_dao.session,
            skip=skip,
            limit=limit,
            is_active=is_active
        )

        return TypeAdapter(list[StoreSchemasBase]).validate_python(stores)


    async def get_store_by_id(
        self,
        store_id: int,
        store_status: bool | None = True
    ) -> StoreSchemasBase:
        store = await self.store_dao.get_by_id(
            self.store_dao.session,
            record_id=store_id,
            is_active=store_status
        )

        if store is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="store is not found"
            )

        return StoreSchemasBase.model_validate(store)


    async def get_store_by_name(
        self,
        store_name: str,
        store_status: bool | None = True
    ) -> StoreSchemasBase:
        store = await self.store_dao.get_store_by_name(
            self.store_dao.session,
            store_name,
            store_status
        )

        if store is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="store is not found"
            )

        return StoreSchemasBase.model_validate(store)


    async def create_store(
        self,
        store_data: StoreCreateRequest
    ) -> StoreCreateResponse:
        store_exist = await self.store_dao.get_store_by_name(
            store_data.name,
            True
        )

        if store_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="store already exists"
            )

        created_store = await self.store_dao.create (self.store_dao.session, store_data)

        return StoreCreateResponse.model_validate(created_store)


    async def update_store(
        self,
        store_id: int,
        store_data: StoreUpdateRequest
    ) -> StoreUpdateResponse:
        store = await self.store_dao.get_by_id(self.store_dao.session, store_id, True)

        if store is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="store is not found"
            )

        update_data = store_data.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing_store = await self.store_dao.get_store_by_name(
                update_data["name"],
                True
            )

            if existing_store and existing_store.id != store_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="store name already registered"
                )

        updated_data = await self.store_dao.update(
            self.store_dao.session,
            store_id,
            store_data
        )

        return StoreUpdateResponse.model_validate(updated_data)


    async def deactivate_store(
        self,
        store_id: int
    ) -> StoreDeactivateResponse:
        store = await self.store_dao.get_by_id(self.store_dao.session, store_id, True)

        if store is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="store is not found"
            )

        res = await self.store_dao.update(
            self.store_dao.session,
            store_id,
            StoreUpdateRequest(is_active=False)
        )

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="fatal error during deactivation"
            )

        return StoreDeactivateResponse(id=store_id)


    async def delete_store(
        self,
        store_id: int
    ) -> StoreDeleteResponse:
        db_store = await self.store_dao.get_by_id(
            self.store_dao.session,
            store_id,
            None
        )

        if db_store is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="store is not found"
            )

        res = await self.store_dao.delete(self.store_dao.session, store_id)

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="fatal error during deletion"
            )

        return StoreDeleteResponse(id=store_id)