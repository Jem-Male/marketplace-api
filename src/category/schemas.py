from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from datetime import datetime


class CategorySchemasBase(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    name: Annotated[str, Field(..., min_length=3, max_length=40)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    created_at: datetime
    updated_at: datetime 
    is_active: bool = True
    
    model_config = ConfigDict(from_attributes=True)
    

class CategoryCreateRequest(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=40)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    

class CategoryCreateResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "Category is registered"
    status: str = "success"


class CategoryUpdateRequest(BaseModel):
    name: Annotated[str | None, Field (min_length=3, max_length=40)] = None
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    image: str | None = None
    is_active: bool = True


class CategoryUpdateResponse(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    message: str = "Category is updates"
    status: str = "success"