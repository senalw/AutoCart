import uuid
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session
from src.domain.entity import CartEntity


class CartRepositoryABC(ABC):
    @abstractmethod
    def create_cart(self, session: Session, cart: CartEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_cart(self, session: Session, cart_id: uuid.UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_cart(self, session: Session, cart_id: uuid.UUID) -> Optional[CartEntity]:
        raise NotImplementedError
