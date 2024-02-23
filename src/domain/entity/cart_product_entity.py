import uuid

from sqlalchemy import Column, ForeignKey, Integer, UUID
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from src.domain.entity.base import Base
from src.domain.entity.product_entity import ProductEntity


class CartProductEntity(Base):
    __tablename__ = "cart_product"

    id: uuid.UUID = Column(type_=UUID, primary_key=True)
    cart_id: uuid.UUID = Column(
        ForeignKey("cart.id", ondelete="restrict"), type_=UUID, nullable=False
    )
    product_id: uuid.UUID = Column(
        ForeignKey("product.id", ondelete="restrict"), type_=UUID, nullable=False
    )
    qty: Mapped[int] = MappedColumn(type_=Integer, nullable=False)
    product: Mapped[ProductEntity] = relationship(
        uselist=False,  # one-to-one relationship
        lazy="joined",
        primaryjoin="CartProductEntity.product_id == ProductEntity.id",
    )
