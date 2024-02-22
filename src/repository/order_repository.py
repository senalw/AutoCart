import uuid
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session
from src.domain.entity import OrderEntity


class OrderRepositoryABC(ABC):
    @abstractmethod
    def add_order(self, session: Session, order: OrderEntity) -> None:
        raise NotImplementedError

    def view_order_by_id(
        self, session: Session, order_id: uuid.UUID
    ) -> Optional[OrderEntity]:
        raise NotImplementedError
