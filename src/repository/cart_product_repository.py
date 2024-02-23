import uuid
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session
from src.domain.entity import CartProductEntity


class CartProductRepositoryABC(ABC):
    @abstractmethod
    def add_items_to_cart(
        self, session: Session, cart_product_entity: CartProductEntity
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_item_from_cart(
        self, session: Session, cart_id: uuid.UUID, product_id: uuid.UUID
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_item_in_cart(
        self, session: Session, cart_id: uuid.UUID, product_id: uuid.UUID
    ) -> Optional[CartProductEntity]:
        raise NotImplementedError
