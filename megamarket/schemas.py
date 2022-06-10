from typing import List, Optional
from enum import Enum
from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel


class ShopUnitType(str, Enum):
    offer = 'OFFER'
    category = 'CATEGORY'


class ShopUnit(BaseModel):
    id: uuid4
    name: str
    date: datetime
    parentId: Optional[uuid4] = None
    type: ShopUnitType
    price: Optional[int] = None
    children: List['ShopUnit'] = []


class ShopUnitImport(BaseModel):
    id: uuid4
    name: str
    parentId: Optional[uuid4] = None
    type: ShopUnitType
    price: Optional[int] = None


class ShopUnitImportRequest(BaseModel):
    items = List[ShopUnitImport]
    updateDate = datetime


class ShopUnitStatisticUnit(BaseModel):
    id: uuid4
    name: str
    parentId: Optional[uuid4]
    type: ShopUnitType
    price: Optional[int]
    date: datetime


class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]


class Error(BaseModel):
    code: int
    message: str
