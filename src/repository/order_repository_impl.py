import uuid
from typing import Optional

from sqlalchemy.orm import Session
from src.domain.entity import OrderEntity
from src.repository.order_repository import OrderRepositoryABC


class OrderRepositoryImpl(OrderRepositoryABC):
    def add_order(self, session: Session, order: OrderEntity) -> None:
        session.add(order)

    def view_order_by_id(
        self, session: Session, order_id: uuid.UUID
    ) -> Optional[OrderEntity]:
        return session.query(OrderEntity).filter(OrderEntity.id == order_id).first()
