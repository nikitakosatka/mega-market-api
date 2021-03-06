from typing import List, Optional
from enum import Enum, unique
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, validator, root_validator

from megamarket.utils import (InvalidRequestException,
                              convert_datetime_to_iso8601)


@unique
class ShopUnitType(str, Enum):
    offer = 'OFFER'
    category = 'CATEGORY'


class ShopUnit(BaseModel):
    id: UUID
    name: str
    date: datetime
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None
    children: Optional[List['ShopUnit']] = None

    @validator('children')
    def empty_list_to_none(cls, v):
        if not v:
            return None

        return v

    class Config:
        orm_mode = True

        json_encoders = {
            datetime: lambda dt: convert_datetime_to_iso8601(dt)
        }


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None

    @root_validator
    def category_price_must_be_null(cls, v):
        if v['type'] == ShopUnitType['category'] and v.get('price'):
            raise InvalidRequestException('Category price must be null')

        if v['type'] == ShopUnitType['offer'] and v.get('price', -1) < 0:
            raise InvalidRequestException(
                'Offer price must be greater of equal to zero')

        return v


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport] = []
    updateDate: datetime

    @validator('items')
    def must_not_contain_same_ids(cls, v):
        request_ids_set = set(item.id for item in v)

        if len(request_ids_set) != len(v):
            raise InvalidRequestException(
                'Request must not contain elements with the same ID')

        return v


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID]
    type: ShopUnitType
    price: Optional[int]
    date: datetime


class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit] = []


class Error(BaseModel):
    code: int
    message: str
