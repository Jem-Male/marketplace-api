from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from datetime import datetime


Str100 = Annotated[str, Field(min_length=2, max_length=100)]
PositiveInt = Annotated[int, Field(gt=0)]


class StoreSchemasBase(BaseModel):
    id: PositiveInt
    name: Str100
    description: Annotated[str | None, Field(max_length=1000)] = None
    image: Annotated[str | None, Field(max_length=2048)] = None
    phone: Annotated[str | None, Field(min_length=7, max_length=20)] = None
    email: EmailStr | None = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class StoreCreateRequest(BaseModel):
    name: Str100
    description: Annotated[str | None, Field(max_length=1000)] = None
    image: Annotated[str | None, Field(max_length=2048)] = None
    phone: Annotated[str | None, Field(min_length=7, max_length=20)] = None
    email: EmailStr | None = None
    
    model_config = ConfigDict(from_attributes=True)


class StoreUpdateRequest(BaseModel):
    name: Annotated[str | None, Field(min_length=2, max_length=100)] = None
    description: Annotated[str | None, Field(max_length=1000)] = None
    image: Annotated[str | None, Field(max_length=2048)] = None
    phone: Annotated[str | None, Field(min_length=7, max_length=20)] = None
    email: EmailStr | None = None
    is_active: bool | None = None  # <--- ВАЖНОЕ ИСПРАВЛЕНИЕ!
    
    model_config = ConfigDict(from_attributes=True)


class StoreCreateResponse(BaseModel):
    id: PositiveInt
    message: str = "Store is created"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)


class StoreUpdateResponse(BaseModel):
    id: PositiveInt
    message: str = "Store is updated"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)
    

class StoreDeactivateResponse(BaseModel):
    id: PositiveInt
    message: str = "Store has been deactivated"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)


class StoreDeleteResponse(BaseModel):
    id: PositiveInt
    message: str = "Store has been HARD deleted!"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)