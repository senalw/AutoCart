import uuid
from typing import Optional

from sqlalchemy.orm import Session
from src.domain.entity import CartEntity
from src.repository.cart_repository import CartRepositoryABC


class CartRepositoryImpl(CartRepositoryABC):
    def create_cart(self, session: Session, cart: CartEntity) -> None:
        session.add(cart)

    def delete_cart(self, session: Session, cart_id: uuid.UUID) -> int:
        return session.query(CartEntity).filter(CartEntity.id == cart_id).delete()

    def get_cart(self, session: Session, cart_id: uuid.UUID) -> Optional[CartEntity]:
        return session.query(CartEntity).filter(CartEntity.id == cart_id).first()
