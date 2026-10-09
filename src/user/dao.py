from sqlalchemy import select, delete, update
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.model import UserModel
from src.dao.base import BaseDAO
from src.user.schemas import UserRegisterRequest, UserUpdateRequest


class UserDAO(BaseDAO[UserModel, UserRegisterRequest, UserUpdateRequest]):
    
    model = UserModel

    async def get_user_by_phone(self, user_phone: str, is_active: bool | None = None) -> UserModel | None:
        query = select(UserModel).where(UserModel.number==user_phone)
        if is_active is not None:
            query = query.where(UserModel.is_active==is_active)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def get_user_by_email(self, user_email: str, is_active: bool | None = None) -> UserModel | None:
        query = select(UserModel).where(UserModel.email==user_email)
        if is_active is not None:
            query = query.where(UserModel.is_active==is_active)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()