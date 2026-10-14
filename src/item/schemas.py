from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from datetime import datetime
from decimal import Decimal

from src.category.schemas import CategorySchemasBase
from src.user.schemas import UserSchemasBase
from src.store.schemas import StoreSchemasBase


class ItemBaseSchema(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=100)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    image: str | None = None
    category: Annotated[int | None, Field(gt=0)] = None
    store: Annotated[int | None, Field(gt=0)] = None
    creator: Annotated[int, Field(gt=0)]


class ItemCreateSchema(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=100)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    image: str | None = None
    category: Annotated[int | None, Field(gt=0)] = None
    store: Annotated[int | None, Field(gt=0)] = None
    stock: Annotated[int, Field(ge=0)] = 1
    is_active: bool = True


class ItemCreateSchemaDB(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=100)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    image: str | None = None
    category: Annotated[int | None, Field(gt=0)] = None
    store: Annotated[int | None, Field(gt=0)] = None
    creator: Annotated[int, Field(gt=0)]
    stock: Annotated[int, Field(ge=0)] = 1
    is_active: bool = True


class ItemResponseSchema(ItemBaseSchema):
    id: Annotated[int, Field(gt=0)]
    created_at: datetime
    updated_at: datetime
    
    creator: Annotated[int, Field(gt=0)]
    store: Annotated[int, Field(gt=0)]
    
    model_config = ConfigDict(from_attributes=True)


class ItemUpdaiteSchema(BaseModel):
    name: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    price: Annotated[Decimal | None, Field(gt=0, max_digits=10, decimal_places=2)] = None
    image: str | None = None
    category: Annotated[int | None, Field(gt=0)] = None
    store: Annotated[int | None, Field(gt=0)] = None
    stock: Annotated[int | None, Field(ge=0)] = None
    is_active: bool | None = None