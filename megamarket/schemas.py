from typing import List, Optional
from enum import Enum, unique
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


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
    children: List['ShopUnit'] = []

    class Config:
        orm_mode = True


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport] = []
    updateDate: datetime


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
