from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from src.item.dao import ItemDAO
from src.user.service import UserService
from src.category.service import CategoryService
from src.store.service import StoreService
from src.item.schemas import (
    ItemCreateSchema,
    ItemUpdaiteSchema,
    ItemResponseSchema,
    ItemCreateSchemaDB
)
from src.file.file import File
from src.item.model import ItemModel
from src.user.schemas import UserShemaMini
from src.item.exceptions import (
    ItemErrors as ItemEr,
    QueruErrors as QueruEr
)
from src.user.model import UserRole


class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.item_dao = ItemDAO(session)
    
    
    async def get_item_safely(self, item_id: int) -> ItemModel:
        item = await self.item_dao.get_by_id(item_id, is_active = True)
        if not item:
            raise ItemEr.item_not_found()
        
        return item
    
    
    async def create_new_item(self, item_data: ItemCreateSchema, current_user: dict) -> ItemModel:
        if  current_user["role"] == UserRole.CUSTOMER:
            raise ItemEr.user_insufficient_privileges()
        
        await UserService(self.session).get_user_by_id(current_user["id"], UserShemaMini, is_active = True)
        await CategoryService(self.session).get_category_by_id(item_data.category, is_active = True)
        await StoreService(self.session).get_store_by_id(item_data.store, store_status = True)
        
        item_data = ItemCreateSchemaDB(**item_data.model_dump(), creator = current_user["id"])
        return await self.item_dao.create(item_data)

    
    async def get_all_items(
        self, skip: int, limit: int, is_active: bool = True
    ) -> ItemModel:
        if limit < 0 or skip < 0:
            raise QueruEr.bad_query()
        
        return await self.item_dao.get_all(skip, limit, is_active)
    
    
    async def update_item_safely(
        self, item_id: int, item_data: ItemUpdaiteSchema, user: dict
    ) -> ItemModel:
        if user["role"] == UserRole.CUSTOMER:
            raise ItemEr.user_insufficient_privileges()
        
        await self.get_item_safely(item_id)
        
        return await self.item_dao.update(item_id, item_data)
    
    
    async def create_item_image(self, item_id: int, user_data: dict, image: UploadFile) -> str:
        if (
            user_data["role"] != UserRole.ADMIN 
            and 
            user_data["role"] != UserRole.OWNER
            and
            user_data["role"] != UserRole.MANAGER
        ): raise ItemEr.user_insufficient_privileges()

        item = await self.get_item_safely(item_id)
        
        uuid = await File.create_image(image, item.image)
        item.image = uuid
        valid_image = ItemUpdaiteSchema(image = uuid)
        await self.item_dao.update(record_id=item_id, schema=valid_image)
        return uuid
    
    
    async def get_item_image(self, image_uuid):
        image = await File.get_image(image_uuid)
        return image
    
    
    async def deactivate_item_safely(
        self, item_id: int, user: dict
    ) -> bool:
        if user["role"] == UserRole.CUSTOMER:
            raise ItemEr.user_insufficient_privileges()
        
        await self.get_item_safely(item_id)
        
        deactivate_data = ItemUpdaiteSchema(is_active = False)
        
        return await self.item_dao.update(item_id, deactivate_data)
    
    
    async def delete_item_safely(
        self, item_id: int, user: dict
    ) -> bool:
        item = await self.get_item_safely(item_id)
        
        if user["id"] != item.creator and user["role"] == UserRole.CUSTOMER:
            raise ItemEr.user_insufficient_privileges()
        
        return await self.item_dao.delete(item_id)