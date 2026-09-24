from fastapi import HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.schemas import (
    UserSchemasBase,
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
    UserUpdateResponse,
    UserDeleteResponse,
    UserDeleteRequest,
    UserDeactivateResponse,
    UserResponseSchemas
)
from src.user.dao import UserDAO
from src.user.model import UserModel
from src.user.auth import create_access_token, get_current_user
from src.user.security import generate_password_hash, check_password_hash



class UserService:
    def __init__(self, session: AsyncSession):
        self.user_dao = UserDAO(session)
    
    
    async def create_new_user(self, user_data: UserRegisterRequest) -> UserRegisterResponse:
        mail_exist = await self.user_dao.get_active_user_by_email(user_data.email)
        if mail_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email is exits"
            )
        
        phone_exist = await self.user_dao.get_active_user_by_phone(user_data.number)
        if phone_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="phone number is exits"
            )
        
        hashed_password = await generate_password_hash(user_data.password)
        
        dict_user_data = user_data.model_dump(exclude={"password"})
        dict_user_data["hashed_password"] = hashed_password
        
        created_user = await self.user_dao.create_new_user(dict_user_data)
        
        token_data = {
            "sub": str(created_user.id) 
        }
        
        token = await create_access_token(token_data)
        
        return UserRegisterResponse(
            id=created_user.id,
            access_token=token
        )
    
    
    async def get_users(self, skip: int, limit: int) -> list[UserResponseSchemas]:
        if skip < 0 or limit < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bad query"
            )
        
        users = await self.user_dao.get_activs_users(skip, limit)
        
        return TypeAdapter(list[UserResponseSchemas]).validate_python(users)
        

    async def get_active_user_by_id(self, user_id: int) -> UserResponseSchemas:
        user = await self.user_dao.get_active_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id not found"
            )
        return UserResponseSchemas.model_validate(user)

    
    async def get_deactive_user_by_id(self, user_id) -> UserResponseSchemas:
        user = await self.user_dao.get_deactive_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id not found"
            )
        if user.is_active == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is activate"
            )
        return UserResponseSchemas.model_validate(user)
    
    
    async def login_user(self, email_or_phone, password) -> UserLoginResponse:
        
        user = await self.user_dao.get_active_user_by_email(email_or_phone)
        
        if user is None:
            user = await self.user_dao.get_active_user_by_phone(email_or_phone)
        
        if user is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Incorrect email/phone or password"
            )
           
        user_verification = await check_password_hash(password, user.hashed_password)
        
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
            access_token=token,
            token_type="bearer"
        )
    
    
    async def user_update(self, user_id: int, user_data: UserUpdateRequest) -> UserUpdateResponse:
        db_user = await self.user_dao.get_active_user_by_id(user_id)
        
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user in not found"
            )
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        if "email" in update_data:
            exiting_user = await self.user_dao.get_active_user_by_email(update_data["email"])
            if exiting_user and exiting_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="email already registered"
                )
        
        if "password" in update_data:
            update_data["hashed_password"] = await generate_password_hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        updated_data = await self.user_dao.update_user(db_user)
        
        return UserUpdateResponse(
            id=updated_data.id
        )
    
    
    async def delete_user(self, user_id: int, user_data: UserDeleteRequest) -> UserDeleteResponse:
        db_user = await self.user_dao.get_deactive_user_by_id(user_id)
        
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user in not found"
            )
        
        user_verification = await check_password_hash(user_data.password, db_user.hashed_password)
        
        if not user_verification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password is not valid"
            )
        
        res = await self.user_dao.delete_user(user_id)
        
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="fatal delet"
            )
        
        return UserDeleteResponse(id=user_id)


    async def deactivate_user(self, user_id: int, user_data: UserDeleteRequest) -> UserDeactivateResponse:
            db_user = await self.user_dao.get_active_user_by_id(user_id)
            
            if db_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="user in not found"
                )
            
            user_verification = await check_password_hash(user_data.password, db_user.hashed_password)
            
            if not user_verification:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="password is not valid"
                )
            
            res = await self.user_dao.deactivate_user(user_id)
            
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="fatal delet"
                )
            
            return UserDeactivateResponse(id=user_id)