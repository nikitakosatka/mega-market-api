from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM, TIMESTAMP
from sqlalchemy import Column, Integer, String, ForeignKey

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
    date = Column(TIMESTAMP(timezone=False), nullable=False)
    children = relationship('ShopUnit', cascade="all, delete", lazy='joined')
