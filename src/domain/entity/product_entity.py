import uuid

from sqlalchemy.orm import MappedColumn, Mapped

from src.domain.entity.base import Base
from sqlalchemy import Column, UUID, Float, Integer, String


class ProductEntity(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = MappedColumn(type_=UUID, primary_key=True)
    name: Mapped[str] = MappedColumn(type_=String, nullable=False)
    price: Mapped[float] = MappedColumn(type_=Float, nullable=False)
    description: Mapped[str] = MappedColumn(type_=String, nullable=True)
    qty: Mapped[int] = MappedColumn(type_=Integer, nullable=False)
