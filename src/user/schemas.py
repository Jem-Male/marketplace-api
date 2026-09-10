from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from datetime import datetime


class UserSchemasBase(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(..., min_length=8, max_length=100)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    created_at: datetime
    updated_at: datetime 
    is_active: bool = True
    

class UserRegisterRequest(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(..., min_length=8, max_length=100)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None


class UserRegisterResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user is registered"
    status: str = "success"
    token: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(..., min_length=8, max_length=100)]


class UserLoginResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user has logged"
    status: str = "success"
    token: str


class UserUpdateRequest(BaseModel):
    name: Annotated[str | None, Field (min_length=3, max_length=100)] = None
    password: Annotated[str | None, Field (min_length=8, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    is_active: bool = True


class UserUpdateResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user is updates"
    status: str = "success"