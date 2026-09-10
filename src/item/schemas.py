from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from datetime import datetime
from decimal import Decimal

# from src.category import 
# from src.user import UserShortSchema
# from src.store import StoreShortSchema


class ItemBaseSchema(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=100)]
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    image: str | None = None
    category: Annotated[int | None, Field(gt=0)] = None
    store_id: Annotated[int | None, Field(gt=0)] = None
    creator: Annotated[int, Field(gt=0)]
    store: Annotated[int, Field(gt=0)]


class ItemCreateSchema(ItemBaseSchema):
    stock: Annotated[int, Field(ge=0)] = 1
    is_active: bool = True


class ItemResponseSchema(ItemBaseSchema):
    id: Annotated[int, Field(gt=0)]
    created_at: datetime
    updated_at: datetime
    
    # creator: UserShortSchema  
    # store: StoreShortSchema
    
    model_config = ConfigDict(from_attributes=True)


class ItemUpdaiteSchema(BaseModel):
    name: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=0, max_length=1000)] = None
    price: Annotated[Decimal | None, Field(gt=0, max_digits=10, decimal_places=2)] = None
    image: str | None = None
    category: Annotated[int | None, Field(gt=0)] = None
    store_id: Annotated[int | None, Field(gt=0)] = None
    stock: Annotated[int | None, Field(ge=0)] = None
    updated_at: datetime
    is_active: bool | None = None