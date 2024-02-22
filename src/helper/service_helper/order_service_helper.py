import uuid

from sqlalchemy.orm import Session
from src.domain.entity import CartEntity, ProductEntity, CartProductEntity
from src.repository import (
    CartProductRepositoryABC,
    CartRepositoryABC,
    ProductRepositoryABC,
)


class OrderServiceHelper:
    @staticmethod
    def add_to_cart(
        session: Session,
        cart_id: str,
        product_entity: ProductEntity,
        requested_qty: int,
        cart_repository: CartRepositoryABC,
        cart_product_repository: CartProductRepositoryABC,
        product_repository: ProductRepositoryABC,
    ) -> CartEntity:
        try:
            cart_entity: CartEntity = OrderServiceHelper._get_cart_entity(
                session, cart_id, product_entity, requested_qty, cart_repository
            )

            OrderServiceHelper._add_new_products_to_cart(
                session,
                cart_entity.id,
                product_entity.id,
                requested_qty,
                cart_product_repository,
            )
            OrderServiceHelper._reduce_quantity_on_stock(
                session, requested_qty, product_entity, product_repository
            )
            return cart_entity
        finally:
            session.commit()

    @staticmethod
    def _get_cart_entity(
        session: Session,
        cart_id: str,
        product_entity: ProductEntity,
        requested_qty: int,
        cart_repository: CartRepositoryABC,
    ) -> CartEntity:
        cart_entity: CartEntity = cart_repository.get_cart(session, uuid.UUID(cart_id))
        # add new item amount to existing amount.
        amount: int = cart_entity.amount + (product_entity.price * requested_qty)

        cart_entity.__setattr__(CartEntity.amount.key, amount)

        return cart_entity

    @staticmethod
    def _add_new_products_to_cart(
        session: Session,
        cart_id: uuid.UUID,
        product_id: uuid.UUID,
        qty: int,
        cart_product_repository: CartProductRepositoryABC,
    ) -> None:
        cart_product_entity: CartProductEntity = CartProductEntity(
            id=uuid.uuid4(),
            cart_id=cart_id,
            product_id=product_id,
            qty=qty,
        )
        cart_product_repository.add_items_to_cart(session, cart_product_entity)

    @staticmethod
    def _reduce_quantity_on_stock(
        session: Session,
        qty: int,
        product_entity: ProductEntity,
        product_repository: ProductRepositoryABC,
    ) -> None:
        product_entity.__setattr__(ProductEntity.qty.key, (product_entity.qty - qty))
        product_repository.update(session, product_entity)
