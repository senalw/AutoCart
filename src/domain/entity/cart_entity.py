import datetime
import uuid

from sqlalchemy import DateTime, Float, func, UUID
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from src.domain.entity.base import Base
from src.domain.entity.cart_product_entity import CartProductEntity


class CartEntity(Base):
    __tablename__ = "cart"

    id: Mapped[uuid.UUID] = MappedColumn(type_=UUID, primary_key=True)
    created_time: Mapped[datetime.datetime] = MappedColumn(
        type_=DateTime(timezone=True), default=func.now()
    )
    last_modified_time: Mapped[datetime.datetime] = MappedColumn(
        type_=DateTime(timezone=True), default=func.now()
    )
    amount: Mapped[float] = MappedColumn(type_=Float, nullable=False)
    cart_products: Mapped[CartProductEntity] = relationship(
        uselist=True,  # one-to-many relationship
        primaryjoin="CartEntity.id == CartProductEntity.cart_id",
        lazy="joined",
    )
