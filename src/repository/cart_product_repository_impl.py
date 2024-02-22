import uuid
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.domain.entity import CartProductEntity
from src.repository.cart_product_repository import CartProductRepositoryABC


class CartProductRepositoryImpl(CartProductRepositoryABC):
    def add_items_to_cart(
        self, session: Session, cart_product_entity: CartProductEntity
    ) -> None:
        session.add(cart_product_entity)

    def remove_item_from_cart(
        self, session: Session, cart_id: uuid.UUID, product_id: uuid.UUID
    ) -> int:
        return (
            session.query(CartProductEntity)
            .filter(
                and_(
                    CartProductEntity.cart_id == cart_id,
                    CartProductEntity.product_id == product_id,
                )
            )
            .delete()
        )

    def get_item_in_cart(
        self, session: Session, cart_id: uuid.UUID, product_id: uuid.UUID
    ) -> Optional[CartProductEntity]:
        return (
            session.query(CartProductEntity)
            .filter(
                and_(
                    CartProductEntity.cart_id == cart_id,
                    CartProductEntity.product_id == product_id,
                )
            )
            .first()
        )
