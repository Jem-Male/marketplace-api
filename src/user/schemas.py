from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from datetime import datetime
from src.user.model import UserRole
from uuid import UUID, uuid4


class UserSchemasBase(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    number: Annotated[str, Field(..., max_length=15)]
    hashed_password: Annotated[str, Field(..., min_length=8, max_length=100)]
    role: UserRole
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    is_email_verified: bool = False
    is_phone_verified: bool = False
    
    default_delivery_address: Annotated[str | None, Field(max_length=500)] = None

    created_at: datetime
    updated_at: datetime 
    is_active: bool = True
    

class UsersSchemas(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    number: Annotated[str, Field(..., max_length=15)]
    role: UserRole
    image: str | None = None
    is_email_verified: bool = False
    is_phone_verified: bool = False
    
    default_delivery_address: Annotated[str | None, Field(max_length=500)] = None

    created_at: datetime
    updated_at: datetime 
    is_active: bool = True
    
    model_config = ConfigDict(from_attributes=True)


class UserResponseSchemas(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    number: Annotated[str, Field(..., max_length=15)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    created_at: datetime
    updated_at: datetime 
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class UserRegisterRequest(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    number: Annotated[str, Field(..., max_length=15)]
    password: Annotated[str, Field(..., min_length=8, max_length=100)]


class UserRegisterData(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    number: Annotated[str, Field(..., max_length=15)]
    hashed_password: Annotated[str, Field(..., max_length=255)]
    role: UserRole


class UserRegisterResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user is registered"
    status: str = "success"
    access_token: Annotated[str, Field(...)]


class UserLoginRequest(BaseModel):
    number: Annotated[str | None, Field(..., max_length=15)] = None
    email: EmailStr | None = None
    password: Annotated[str, Field(..., min_length=8, max_length=100)]


class UserLoginResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user has logged"
    status: str = "success"
    access_token: str 
    token_type: str = "bearer"


class UserUpdateRequest(BaseModel):
    name: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    number: Annotated[str | None, Field(max_length=15)] = None
    email: EmailStr | None = None
    password: Annotated[str | None, Field(min_length=8, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    default_delivery_address: Annotated[str | None, Field(max_length=500)] = None


class UserShemaMini(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    name: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    number: Annotated[str | None, Field(max_length=15)] = None
    email: EmailStr | None = None
    hashed_password: Annotated[str | None, Field (min_length=8, max_length=100)] = None
    role: UserRole
    is_active: bool | None = None
    
    model_config = ConfigDict(from_attributes=True)


class UserUpdateData(BaseModel):
    name: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    number: Annotated[str | None, Field(max_length=15)] = None
    email: EmailStr | None = None
    hashed_password: Annotated[str | None, Field (min_length=8, max_length=100)] = None
    is_email_verified: bool | None = None
    is_phone_verified: bool | None = None
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    is_active: bool | None = None
    default_delivery_address: Annotated[str | None, Field(max_length=500)] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserUpdateResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user is updates"
    status: str = "success"
    

class UserDeleteRequest(BaseModel):
    password: Annotated[str, Field(..., min_length=8, max_length=100)]


class UserDeleteResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user has deleted"
    status: str = "success"


class UserDeactivateResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user has deactivated"
    status: str = "success"