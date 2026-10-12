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
from src.user.model import UserRole
from src.user.auth import create_access_token
from src.user.security import generate_password_hash, check_password_hash
from src.user.exceptions import (
    UserErrors as UserEr,
    QueruErrors as QueruEr,
    DBErrors as DBErr
) 


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_dao = UserDAO(session)


    async def get_user_by_id(self, user_id: int, return_schema: Type[BaseModel], is_active: bool | None = None) -> Type[BaseModel]:
        db_user = await self.user_dao.get_by_id(user_id, is_active)
        if db_user is None:
            raise UserEr.user_not_found()
        return return_schema.model_validate(db_user)


    async def get_user_by_email(self, user_email: str, return_schema: Type[BaseModel], is_active: bool):
        db_user = await self.user_dao.get_user_by_email(user_email, is_active)
        if db_user is None:
            raise UserEr.user_not_found()
        
        return return_schema.model_validate(db_user)


    async def get_user_by_phone(self, user_phone: str, return_schema: Type[BaseModel], is_active: bool = True):
        db_user = await self.user_dao.get_user_by_phone(user_phone, is_active)
        if db_user is None:
            raise UserEr.user_not_found()
            
        return return_schema.model_validate(db_user)


    async def create_new_user(self, user_data: UserRegisterRequest) -> UserRegisterResponse:
        mail_exist = await self.user_dao.get_user_by_email(user_data.email, is_active=True)
        if mail_exist is not None:
            raise UserEr.email_is_exits()
        
        phone_exist = await self.user_dao.get_user_by_phone(user_data.number, is_active=True)
        if phone_exist is not None:
            raise UserEr.phone_is_exits()
        
        hashed_password = await generate_password_hash(user_data.password)
        
        dict_user_data = user_data.model_dump(exclude={"password"})
        dict_user_data["hashed_password"] = hashed_password
        dict_user_data["role"] = UserRole.CUSTOMER.value
        
        valid_user_data = UserRegisterData(**dict_user_data)
        
        created_user = await self.user_dao.create(valid_user_data)
        
        token_data = {
            "sub": str(created_user.id),
            "role": str(dict_user_data["role"])
        }
        
        token = await create_access_token(token_data)
        
        return UserRegisterResponse(
            id=created_user.id,
            access_token=token
        )


    async def get_users(self, skip: int, limit: int, is_active: bool | None = None) -> list[UserResponseSchemas]:
        
        if skip < 0 or limit < 0:
            raise QueruEr.bad_query()
        
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
            raise UserEr.valid_password()
        token_data = {
            "sub": str(user.id),
            "role": user.role
        }   
        token = await create_access_token(token_data)    
        
        return UserLoginResponse(
            id=user.id,
            access_token=token,
            token_type="bearer"
        )


    async def user_update(self, current_user_id: int, user_id: int, user_data: UserUpdateRequest) -> UserUpdateResponse:
        if current_user_id is not user_id:
            raise UserEr.insufficient_privileges()

        await self.get_user_by_id(user_id, UserResponseSchemas)
        update_data = user_data.model_dump(exclude_unset=True)
        
        if "email" in update_data:
            exiting_user = await self.user_dao.get_user_by_email(update_data["email"])
            if exiting_user and exiting_user.id != user_id:
                raise UserEr.email_already_registered()
        
        if "number" in update_data:
            phone_exist = await self.user_dao.get_user_by_phone(update_data["number"])
            if phone_exist is not None and phone_exist.id != user_id:
                raise UserEr.email_already_registered()
        
        if "password" in update_data:
            update_data["hashed_password"] = await generate_password_hash(update_data.pop("password"))
        
        valid_update_user = UserUpdateData(**update_data)
        updated_data = await self.user_dao.update(record_id=user_id, schema=valid_update_user)
        
        return UserUpdateResponse(
            id=updated_data.id
        )


    async def delete_user(self, user_id: int, user_data: UserDeleteRequest) -> UserDeleteResponse:
        db_user = await self.get_user_by_id(user_id, UserShemaMini)
        
        if db_user.role is not UserRole.ADMIN:
            raise UserEr.insufficient_privileges()
        
        user_verification = await check_password_hash(user_data.password, db_user.hashed_password)
        
        if not user_verification:
            raise UserEr.invalid_password()
        
        res = await self.user_dao.delete(user_id)
        
        if not res:
            raise DBErr.fatal_delet()
        
        return UserDeleteResponse(id=user_id)


    async def deactivate_user(self, user_id: int, user_data: UserDeleteRequest) -> UserDeactivateResponse:
        db_user = await self.get_user_by_id(user_id, UserShemaMini, True)
        user_verification = await check_password_hash(user_data.password, db_user.hashed_password)

        if not user_verification:
            raise UserEr.invalid_password()
        
        db_user.is_active = False
    
        res = await self.user_dao.update(user_id, db_user)
        
        if not res:
            raise DBErr.fatal_deactivaite()
        
        return UserDeactivateResponse(id=user_id)