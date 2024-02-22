import uuid
from datetime import datetime

from src.domain.entity import CartEntity
from src.domain.entity.base import Base
from sqlalchemy import DateTime, Float, ForeignKey, String, UUID
from sqlalchemy.orm import relationship, Mapped, MappedColumn


class OrderEntity(Base):
    __tablename__ = "order"

    id: Mapped[uuid.UUID] = MappedColumn(type_=UUID, primary_key=True)
    cart_id: Mapped[uuid.UUID] = MappedColumn(
        ForeignKey("cart.id"), type_=UUID, nullable=False
    )
    total_amount: Mapped[float] = MappedColumn(type_=Float, nullable=False)
    delivery_address: Mapped[str] = MappedColumn(type_=String, nullable=False)
    delivery_time: Mapped[datetime] = MappedColumn(
        type_=DateTime(timezone=True), nullable=False
    )
    delivery_status: Mapped[str] = MappedColumn(
        type_=String, nullable=False, default="PENDING"
    )

    cart_entity: Mapped[CartEntity] = relationship(
        uselist=False,  # one-to-one relationship
        primaryjoin="OrderEntity.cart_id == CartEntity.id",
        lazy="joined",
    )
