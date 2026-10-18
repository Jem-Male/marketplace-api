from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
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
    UserResponseSchemas,
    UsersSchemas
)
from src.user.service import UserService
from src.database import get_db
from src.user.auth import get_current_user
from src.user.model import UserRole


user_router = APIRouter(
    tags=["Users"]
)


@user_router.get(
    '/all',
    response_model = list[UsersSchemas],
    summary="get list users"
)
async def get_users(
    skip: int = 0,
    limit: int = 10000,
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
    res = await UserService(session).get_users(skip, limit, is_active=True)
    return res


@user_router.get("/image/{image_uuid}")
async def get_user_image(
    image_uuid: str,
    session = Depends(get_db) 
):
   res = await UserService(session).get_user_image(image_uuid)
   return res


@user_router.get('/{user_id}', response_model=UserResponseSchemas)
async def get_active_user(
    user_id: int,
    session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if (
        current_user["id"] != user_id and
        current_user["role"] != UserRole.ADMIN and
        current_user["role"] != UserRole.MANAGER and
        current_user["role"]  != UserRole.OWNER
    ):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
    
    res = await UserService(session).get_user_by_id(user_id, UserResponseSchemas, True)
    return res


@user_router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: UserRegisterRequest, session = Depends(get_db)):
    res = await UserService(session).create_new_user(user_data)
    return res


@user_router.post("/login", response_model=UserLoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    res = await UserService(session).login_user(
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
    if (
        current_user["id"] != user_id
        and
        current_user["role"] != UserRole.ADMIN
    ):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not priveleges"
        )
    res = await UserService(session).user_update(user_id, user_data)
    return res


@user_router.post("/image", status_code = status.HTTP_201_CREATED)
async def create_user_image(
    file: UploadFile,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    image_name = await UserService(session).create_user_image(current_user["id"], file)
    return {
        "message": "Successfully created",
        "image name": f"{image_name}"
    }


@user_router.patch("/deactivate/{user_id}", response_model=UserDeactivateResponse)
async def user_deactivate(
    user_id: int, 
    user_data: UserDeleteRequest,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    if (
        current_user["id"] != user_id 
        and
        current_user["role"] != UserRole.ADMIN
    ):
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough privileges"
            )
    res = await UserService(session).deactivate_user(user_id, user_data)
    return res


@user_router.delete("/delete/{user_id}", response_model=UserDeleteResponse)
async def user_delete(
    user_id: int, 
    user_data: UserDeleteRequest,
    current_user = Depends(get_current_user),
    session = Depends(get_db)
):
    res = await UserService(session).delete_user(user_id, user_data, current_user)
    return res
