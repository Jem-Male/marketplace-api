# from decimal import Decimal
# from src.dao.base import BaseDAO
# from src.item.model import ItemModel
# from src.item.schemas import ItemCreateSchema, ItemResponseSchema
# from sqlalchemy import select


# class ItemDAO(BaseDAO[ItemModel, ItemCreateSchema, ItemResponseSchema]):
#     async def get_items_by_price_range(self, session, min_price: Decimal, max_price: Decimal):
#         result = await session.execute(
#             select(self.model)
#             .where(self.model.price.between(min_price,max_price))
#         )
#         return result.scalars().all()




from sqlalchemy import select
from src.database import AsyncSessionLocal, get_db
from src.user.model import UserModel


class UserDAO:
    
    def __init__(self, database):
        self.database = database
    
    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(UserModel).where(UserModel.id==user_id))
            return res.scalar_one_or_none()

    
    async def get_user_by_email(self, user_email: str) -> UserModel | None:
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(UserModel).where(UserModel.email==user_email))
            return res.scalar_one_or_none()

    
    async def create_new_user(self, user_data_dict: dict) -> UserModel:
        async with AsyncSessionLocal() as session:
            db_user = UserModel(**user_data_dict)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user
    
    
    async def update_user(self, user_id:int, user_data_dict: dict) -> UserModel:
        async with AsyncSessionLocal() as session:
            db_user = await session.get(UserModel, user_id)
            
            if not db_user:
                return None
            
            for key, value in user_data_dict.items():
                setattr(db_user, key, value)
            
            await session.commit()
            await session.refresh(db_user)
            return db_user
