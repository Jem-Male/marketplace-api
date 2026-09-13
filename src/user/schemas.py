from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from datetime import datetime


class UserSchemasBase(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: EmailStr
    number: Annotated[str, Field(..., max_length=15)]
    password: Annotated[str, Field(..., min_length=8, max_length=100)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    created_at: datetime
    updated_at: datetime 
    is_active: bool = True
    

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
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None


class UserRegisterResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user is registered"
    status: str = "success"
    token: str


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
    name: Annotated[str | None, Field (min_length=3, max_length=100)] = None
    number: Annotated[str | None, Field(..., max_length=15)] = None
    email: EmailStr | None = None
    password: Annotated[str | None, Field (min_length=8, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    is_active: bool = True


class UserUpdateResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user is updates"
    status: str = "success"
    

class UserDeleteRequest(BaseModel):
    password: Annotated[str, Field(..., min_length=8, max_length=100)]


class UserDeleteResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user has HARD DELETED"
    status: str = "success"


class UserDeactivateResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "user has deleted"
    status: str = "success"