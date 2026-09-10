from fastapi import APIRouter
from src.user.schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
    UserUpdateResponse
)
from src.user.service import UserService


user_router = APIRouter(
    tags=["Users"]
)

userService = UserService()

@user_router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: UserRegisterRequest):
    res = await userService.create_new_user(user_data)
    return res


@user_router.post("/login", response_model=UserLoginResponse)
async def login(user_data: UserLoginRequest):
    res = await userService.login_user(user_data)
    return res


@user_router.get('/user/{user_id}')
async def get_info(user_id: int):
    # res = await get_user_by_id()
    return 


@user_router.patch("/update/{user_id}", response_model=UserUpdateResponse)
async def update_user(user_id: int, user_data: UserUpdateRequest):
    res = await userService.user_update(user_id, user_data)
    return res