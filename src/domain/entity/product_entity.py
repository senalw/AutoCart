import uuid

from sqlalchemy import Float, Integer, String, UUID
from sqlalchemy.orm import Mapped, MappedColumn
from src.domain.entity.base import Base


class ProductEntity(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = MappedColumn(type_=UUID, primary_key=True)
    name: Mapped[str] = MappedColumn(type_=String, nullable=False)
    price: Mapped[float] = MappedColumn(type_=Float, nullable=False)
    description: Mapped[str] = MappedColumn(type_=String, nullable=True)
    qty: Mapped[int] = MappedColumn(type_=Integer, nullable=False)
