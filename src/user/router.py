from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 

from src.user.schemas import (
    UserSchemasBase,
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
    UserUpdateResponse,
    UserDeleteResponse,
    UserDeactivateResponse,
    UserDeleteRequest,
    UserResponseSchemas
)
from src.user.service import UserService
from src.database import get_db
from src.user.auth import create_access_token, get_current_user


user_router = APIRouter(
    tags=["Users"]
)


@user_router.get('/all')
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session = Depends(get_db)
):
    userService = UserService(session)
    res = await userService.get_users(skip, limit)
    return res


@user_router.get('/{user_id}', response_model=UserResponseSchemas)
async def get_active_user(user_id: int, session = Depends(get_db)):
    userService = UserService(session)
    res = await userService.get_active_user_by_id(user_id)
    return res


@user_router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: UserRegisterRequest, session = Depends(get_db)):
    userService = UserService(session)
    res = await userService.create_new_user(user_data)
    return res


@user_router.post("/login", response_model=UserLoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    userService = UserService(session)
    res = await userService.login_user(
        email_or_phone = form_data.username,
        password = form_data.password
    )
    return res


@user_router.patch("/update/{user_id}", response_model=UserUpdateResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    if current_user != user_id:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough privileges"
            )
    userService = UserService(session)
    res = await userService.user_update(user_id, user_data)
    return res


@user_router.patch("/deactivate/{user_id}", response_model=UserDeactivateResponse)
async def user_deactivate(
    user_id: int, 
    user_data: UserDeleteRequest,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    if current_user != user_id:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough privileges"
            )
    userService = UserService(session)
    res = await userService.deactivate_user(user_id, user_data)
    return res


@user_router.delete("/delete/{user_id}", response_model=UserDeleteResponse)
async def user_delete(
    user_id: int, 
    user_data: UserDeleteRequest,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    if current_user != user_id:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough privileges"
            )
    userService = UserService(session)
    res = await userService.delete_user(user_id, user_data)
    return res


@user_router.get('/deactive/{user_id}', response_model=UserResponseSchemas)
async def get_deactive_user(
    user_id: int,
    session = Depends(get_db)
):
    userService = UserService(session)
    res = await userService.get_deactive_user_by_id(user_id)
    return res