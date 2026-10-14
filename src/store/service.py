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
from src.store.exceptions import(
    StoreErrors as StoreEr,
    QueruErrors as QueruEr,
    DBErrors as DBEr
)
from src.user.model import UserRole


class StoreService:
    def __init__(self, session: AsyncSession):
        self.store_dao = StoreDAO(session)
        self.session = session


    async def get_all_stores(
        self,
        skip: int,
        limit: int,
        is_active: bool | None = None
    ) -> list[StoreSchemasBase]:
        if skip < 0 or limit <= 0 or limit < skip:
            raise QueruEr.bad_query()

        stores = await self.store_dao.get_all(
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
            record_id=store_id,
            is_active=store_status
        )

        if store is None:
            raise StoreEr.not_found()

        return StoreSchemasBase.model_validate(store)


    async def get_store_by_name(
        self,
        store_name: str,
        store_status: bool | None = True
    ) -> StoreSchemasBase:
        store = await self.store_dao.get_store_by_name(
            store_name,
            store_status
        )

        if store is None:
            raise StoreEr.not_found()

        return StoreSchemasBase.model_validate(store)


    async def create_store(
        self,
        store_data: StoreCreateRequest,
        current_user: dict
    ) -> StoreCreateResponse:
        
        if (
            current_user["role"] != UserRole.ADMIN
            and
            current_user["role"] != UserRole.OWNER
        ):
            raise StoreEr.user_insufficient_privileges()
        
        store_exist = await self.store_dao.get_store_by_name(store_data.name, True)

        if store_exist is not None:
            raise StoreEr.already_exists()

        created_store = await self.store_dao.create(store_data)

        return StoreCreateResponse.model_validate(created_store)


    async def update_store(
        self,
        store_id: int,
        store_data: StoreUpdateRequest,
        current_user: dict
    ) -> StoreUpdateResponse:
        if (
            current_user["role"] != UserRole.ADMIN
            and
            current_user["role"] != UserRole.OWNER
        ):
            raise StoreEr.user_insufficient_privileges()
        
        await self.get_store_by_id(store_id, True)

        update_data = store_data.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing_store = await self.store_dao.get_store_by_name(update_data["name"], True)

            if existing_store and existing_store.id != store_id:
                raise StoreEr.already_exists()

        updated_data = await self.store_dao.update(store_id, store_data)

        return StoreUpdateResponse.model_validate(updated_data)


    async def deactivate_store(
        self,
        store_id: int,
        current_user: dict
    ) -> StoreDeactivateResponse:
        if (
            current_user["role"] != UserRole.ADMIN
            and
            current_user["role"] != UserRole.OWNER
        ):
            raise StoreEr.user_insufficient_privileges()
        
        await self.get_store_by_id(store_id, True)

        res = await self.store_dao.update(store_id, StoreUpdateRequest(is_active=False))

        if not res:
            raise DBEr.fatal_deactivaite()

        return StoreDeactivateResponse(id=store_id)


    async def delete_store(
        self,
        store_id: int,
        current_user: dict
    ) -> StoreDeleteResponse:
        
        if current_user["role"] != UserRole.ADMIN:
            raise StoreEr.user_insufficient_privileges()
        
        await self.get_store_by_id(store_id ,None)

        res = await self.store_dao.delete(store_id)

        if not res:
            raise DBEr.fatal_delet()

        return StoreDeleteResponse(id=store_id)