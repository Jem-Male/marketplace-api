# from fastapi import HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.item.dao import ItemDAO
# from src.item.schemas import ItemCreateSchema, ItemUpdaiteSchema, ItemResponseSchema
# from src.item.model import ItemModel



# class ItemService:
#     @classmethod
#     async def create_new_item(
#         cls, session: AsyncSession, item_data: ItemCreateSchema, user_id: int
#     ) -> ItemModel:

#         user_items = await ItemDAO.get_items_by_owner(session, owner_id=user_id)
                    
#         full_data = item_data.model_dump()
#         full_data["owner_id"] = user_id
        
#         return await ItemDAO.create(session, item_data)

#     @classmethod
#     async def get_item_safely(cls, session: AsyncSession, item_id: int) -> ItemModel:
#         item = await ItemDAO.get_by_id(session, item_id)
#         if not item:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Товар с ID {item_id} не найден."
#             )
#         return item



from fastapi import HTTPException, status

from src.user.schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
    UserUpdateResponse
)
from src.user.dao import UserDAO
from src.user.model import UserModel
from src.user.auth import create_access_token, get_current_user
from src.user.security import generate_password_hash, check_password_hash


userDAO = UserDAO(UserModel)


class UserService:
    async def create_new_user(self, user_data: UserRegisterRequest) -> UserRegisterResponse:
        mail_exist = await userDAO.get_user_by_email(user_data.email)
        if mail_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email is exits"
            )
        
        hashed_password = await generate_password_hash(user_data.password)
        
        dict_user_data = user_data.model_dump(exclude={"password"})
        dict_user_data["hashed_password"] = hashed_password
        
        created_user = await userDAO.create_new_user(dict_user_data)
        
        token_data = {
            "sub": str(created_user.id) 
        }
        
        token = await create_access_token(token_data)
        
        return UserRegisterResponse(
            id=created_user.id,
            token=token
        )
        
    
    async def login_user(self, user_data: UserLoginRequest) -> UserLoginResponse:
        user = await userDAO.get_user_by_email(user_data.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email not found"
            )
        
        user_verification = await check_password_hash(user_data.password, user.hashed_password)
        
        if not user_verification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password is not valid"
            )
        
        token_data = {
            "sub": str(user.id) 
        }
                
        token = await create_access_token(token_data)    
        
        return UserLoginResponse(
            id=user.id,
            token=token
        )
    
    
    async def user_update(self, user_id: int, user_data: UserUpdateRequest) -> UserUpdateResponse:
        user = await userDAO.get_user_by_id(user_id)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user in not found"
            )
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        if "email" in user_data:
            exiting_user = await userDAO.get_user_by_email(update_data["email"])
            if exiting_user and exiting_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="email already registered"
                )
        
        if "password" in update_data:
            update_data["hashed_password"] = await generate_password_hash(update_data.pop("password"))
        
        updated_data = await userDAO.update_user(user_id, update_data)
        
        return UserUpdateResponse(
            id=updated_data.id
        )
    
    