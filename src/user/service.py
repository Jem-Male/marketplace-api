from fastapi import HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
from pydantic import BaseModel

from src.user.schemas import (
    UserSchemasBase,
    UserRegisterRequest,
    UserRegisterData,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
    UserUpdateData,
    UserShemaMini,
    UserUpdateResponse,
    UserDeleteResponse,
    UserDeleteRequest,
    UserDeactivateResponse,
    UserResponseSchemas
)
from src.user.dao import UserDAO
from src.user.model import UserModel
from src.user.auth import create_access_token
from src.user.security import generate_password_hash, check_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_dao = UserDAO(session)


    async def get_user_by_id(self, user_id: int, return_schema: Type[BaseModel], is_active: bool | None = None) -> Type[BaseModel]:
        db_user = await self.user_dao.get_by_id(user_id, is_active)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
        return return_schema.model_validate(db_user)


    async def get_user_by_email(self, user_email: str, return_schema: Type[BaseModel], is_active: bool):
        db_user = await self.user_dao.get_user_by_email(user_email, is_active)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user in not found"
            )
        
        return return_schema.model_validate(db_user)


    async def get_user_by_phone(self, user_phone: str, return_schema: Type[BaseModel], is_active: bool = True):
        db_user = await self.user_dao.get_user_by_phone(user_phone, is_active)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user in not found"
            )
        
        return return_schema.model_validate(db_user)


    async def create_new_user(self, user_data: UserRegisterRequest) -> UserRegisterResponse:
        mail_exist = await self.user_dao.get_user_by_email(user_data.email, is_active=True)
        if mail_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email is exits"
            )
        
        phone_exist = await self.user_dao.get_user_by_phone(user_data.number, is_active=True)
        if phone_exist is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="phone number is exits"
            )
        
        hashed_password = await generate_password_hash(user_data.password)
        
        dict_user_data = user_data.model_dump(exclude={"password"})
        dict_user_data["hashed_password"] = hashed_password
        
        valid_user_data = UserRegisterData(**dict_user_data)
        
        created_user = await self.user_dao.create(valid_user_data)
        
        token_data = {
            "sub": str(created_user.id) 
        }
        
        token = await create_access_token(token_data)
        
        return UserRegisterResponse(
            id=created_user.id,
            access_token=token
        )


    async def get_users(self, skip: int, limit: int, is_active: bool | None = None) -> list[UserResponseSchemas]:
        if skip < 0 or limit < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bad query"
            )
        
        users = await self.user_dao.get_all(skip, limit, is_active)
        
        return TypeAdapter(list[UserResponseSchemas]).validate_python(users)


    async def login_user(self, email_or_phone: str, password: str) -> UserLoginResponse:
        
        user = await self.user_dao.get_user_by_email(email_or_phone, is_active=True)
        
        if user is None:
            user = await self.user_dao.get_user_by_phone(email_or_phone, is_active=True)
        
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
        await self.get_user_by_id(user_id, UserResponseSchemas)

        update_data = user_data.model_dump(exclude_unset=True)
        
        if "email" in update_data:
            exiting_user = await self.user_dao.get_user_by_email(update_data["email"])
            if exiting_user and exiting_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="email already registered"
                )
        
        if "number" in update_data:
            phone_exist = await self.user_dao.get_user_by_phone(update_data["number"])
            if phone_exist is not None and phone_exist.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="phone number is exits"
                )
        
        if "password" in update_data:
            update_data["hashed_password"] = await generate_password_hash(update_data.pop("password"))
        
        valid_update_user = UserUpdateData(**update_data)
        
        updated_data = await self.user_dao.update(record_id=user_id, schema=valid_update_user)
        
        return UserUpdateResponse(
            id=updated_data.id
        )


    async def delete_user(self, user_id: int, user_data: UserDeleteRequest) -> UserDeleteResponse:
        db_user = await self.get_user_by_id(user_id, UserShemaMini)
        
        user_verification = await check_password_hash(user_data.password, db_user.hashed_password)
        
        if not user_verification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password is not valid"
            )
        
        res = await self.user_dao.delete(user_id)
        
        if not res:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="fatal delet"
            )
        
        return UserDeleteResponse(id=user_id)


    async def deactivate_user(self, user_id: int, user_data: UserDeleteRequest) -> UserDeactivateResponse:
        db_user = await self.get_user_by_id(user_id, UserShemaMini, True)
        
        user_verification = await check_password_hash(user_data.password, db_user.hashed_password)
        
        if not user_verification:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="password is not valid"
            )
        
        db_user.is_active = False
        
        res = await self.user_dao.update(user_id, db_user)
        
        if not res:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="fatal deactivate"
            )
        
        return UserDeactivateResponse(id=user_id)