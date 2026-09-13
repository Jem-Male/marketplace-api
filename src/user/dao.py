from sqlalchemy import select, delete, update
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionLocal, get_db
from src.user.model import UserModel

class UserDAO:
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_active_user_by_id(self, user_id: int) -> UserModel | None:
        res = await self.session.execute(select(UserModel).where(UserModel.id==user_id, UserModel.is_active==True))
        return res.scalar_one_or_none()


    async def get_active_user_by_phone(self, user_phone: str) -> UserModel | None:
        res = await self.session.execute(select(UserModel).where(UserModel.number==user_phone, UserModel.is_active==True))
        return res.scalar_one_or_none()
    
    
    async def get_deactive_user_by_id(self, user_id: int) -> UserModel | None:
        res = await self.session.execute(select(UserModel).where(UserModel.id==user_id))
        return res.scalar_one_or_none()
    
    
    async def get_active_user_by_email(self, user_email: str) -> UserModel | None:
        res = await self.session.execute(select(UserModel).where(UserModel.email==user_email, UserModel.is_active==True))
        return res.scalar_one_or_none()

    
    async def get_activs_users(self, skip: int=0, limit: int=100) -> Sequence[UserModel]:
        res = await self.session.execute(
            select(UserModel).where(UserModel.is_active==True).offset(skip).limit(limit)
        )
        return res.scalars().all()

    
    async def create_new_user(self, user_data_dict: dict) -> UserModel:
        db_user = UserModel(**user_data_dict)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    
    async def update_user(self, db_user: UserModel) -> UserModel:
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    
    async def deactivate_user(self, user_id: int) -> bool:
        res = await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(is_active=False)
        )
        await self.session.commit()
        return res.rowcount > 0  

    
    async def delete_user(self, user_id: int) -> bool:
        res = await self.session.execute(delete(UserModel).where(UserModel.id==user_id))
        await self.session.commit()
        return res.rowcount > 0