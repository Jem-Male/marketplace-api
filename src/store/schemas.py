from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated, Optional
from datetime import datetime
from enum import Enum


Str100 = Annotated[str, Field(..., min_length=2, max_length=100)]
Str255 = Annotated[str, Field(..., min_length=2, max_length=255)]
Str500 = Annotated[str, Field(..., min_length=5, max_length=500)]
BinIinStr = Annotated[str, Field(..., min_length=12, max_length=12, pattern=r"^\d{12}$")]
BankAccountStr = Annotated[str, Field(..., min_length=20, max_length=34)]
BikStr = Annotated[str, Field(..., min_length=8, max_length=11)]
PositiveInt = Annotated[int, Field(..., gt=0)]


class TaxRegime(str, Enum):
    SIMPLIFIED = "simplified"
    COMMON = "common"
    PATENT = "patent"


class StoreSchemasBase(BaseModel):
    id: PositiveInt
    name: Str100
    description: Annotated[str | None, Field(default=None, max_length=1000)] = None
    image: Annotated[str | None, Field(default=None, max_length=2048)] = None
    legal_name: Str255
    bin_iin: BinIinStr
    legal_address: Str500
    tax_regime: TaxRegime
    license_number: Annotated[str | None, Field(default=None, max_length=100)] = None
    bank_account: BankAccountStr
    bank_name: Str255
    bik: BikStr
    physical_address: Str500
    phone: Annotated[str, Field(..., min_length=7, max_length=20)]
    email: EmailStr
    kkm_serial_number: Annotated[str | None, Field(default=None, max_length=50)] = None
    ofd_token: Annotated[str | None, Field(default=None, max_length=255)] = None
    created_at: datetime
    updated_at: datetime 
    is_active: bool = True
    
    model_config = ConfigDict(from_attributes=True)


class StoreCreateRequest(BaseModel):
    name: Str100
    description: Annotated[str | None, Field(default=None, max_length=1000)] = None
    image: Annotated[str | None, Field(default=None, max_length=2048)] = None
    legal_name: Str255
    bin_iin: BinIinStr
    legal_address: Str500
    tax_regime: TaxRegime
    license_number: Annotated[str | None, Field(default=None, max_length=100)] = None
    bank_account: BankAccountStr
    bank_name: Str255
    bik: BikStr
    physical_address: Str500
    phone: Annotated[str, Field(..., min_length=7, max_length=20)]
    email: EmailStr
    kkm_serial_number: Annotated[str | None, Field(default=None, max_length=50)] = None
    ofd_token: Annotated[str | None, Field(default=None, max_length=255)] = None
    
    model_config = ConfigDict(from_attributes=True)


class StoreUpdateRequest(BaseModel):
    name: Annotated[str | None, Field(default=None, min_length=2, max_length=100)] = None
    description: Annotated[str | None, Field(default=None, max_length=1000)] = None
    image: Annotated[str | None, Field(default=None, max_length=2048)] = None
    legal_name: Annotated[str | None, Field(default=None, min_length=2, max_length=255)] = None
    bin_iin: Annotated[str | None, Field(default=None, min_length=12, max_length=12, pattern=r"^\d{12}$")] = None
    legal_address: Annotated[str | None, Field(default=None, min_length=5, max_length=500)] = None
    tax_regime: Optional[TaxRegime] = None
    license_number: Annotated[str | None, Field(default=None, max_length=100)] = None
    bank_account: Annotated[str | None, Field(default=None, min_length=20, max_length=34)] = None
    bank_name: Annotated[str | None, Field(default=None, min_length=2, max_length=255)] = None
    bik: Annotated[str | None, Field(default=None, min_length=8, max_length=11)] = None
    physical_address: Annotated[str | None, Field(default=None, min_length=5, max_length=500)] = None
    phone: Annotated[str | None, Field(default=None, min_length=7, max_length=20)] = None
    email: Optional[EmailStr] = None
    kkm_serial_number: Annotated[str | None, Field(default=None, max_length=50)] = None
    ofd_token: Annotated[str | None, Field(default=None, max_length=255)] = None
    is_active: bool = True
    
    model_config = ConfigDict(from_attributes=True)


class StoreCreateResponse(BaseModel):
    id: PositiveInt
    message: str = "Store is created"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)


class StoreUpdateResponse(BaseModel):
    id: PositiveInt
    message: str = "Store is updates"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)
    

class StoreDeactivateResponse(BaseModel):
    id: PositiveInt
    message: str = "store has deleted"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)


class StoreDeleteResponse(BaseModel):
    id: PositiveInt
    message: str = "store has HARD deleted!"
    status: str = "success"
    
    model_config = ConfigDict(from_attributes=True)