from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from megamarket.db import Base
from megamarket.schemas import ShopUnitType


class ShopUnit(Base):
    __tablename__ = 'shop_units'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(ENUM(ShopUnitType), nullable=False)
    parentId = Column(UUID(as_uuid=True), ForeignKey('shop_units.id'),
                      nullable=True)
    price = Column(Integer, nullable=True)
    updateDate = Column(DateTime, nullable=False)
    children = relationship('ShopUnit')
