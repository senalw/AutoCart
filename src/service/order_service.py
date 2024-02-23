import uuid
from datetime import datetime

from src.core.database.postgres_client import PostgresClient
from src.core.exception import NotAvailableError, NotFoundError
from src.domain.entity import CartEntity, OrderEntity, ProductEntity
from src.helper.service_helper import OrderServiceHelper
from src.mapper import EntityToSchemaMapper
from src.repository import (
    CartProductRepositoryABC,
    CartRepositoryABC,
    OrderRepositoryABC,
    ProductRepositoryABC,
)
from src.schema import OrderSchema
from src.schema.cart_schema import CartSchema


class OrderService:
    def __init__(
        self,
        database: PostgresClient,
        cart_repository: CartRepositoryABC,
        cart_product_repository: CartProductRepositoryABC,
        order_repository: OrderRepositoryABC,
        product_repository: ProductRepositoryABC,
    ) -> None:
        self.database: PostgresClient = database
        self.cart_repository: CartRepositoryABC = cart_repository
        self.cart_product_repository: CartProductRepositoryABC = cart_product_repository
        self.order_repository: OrderRepositoryABC = order_repository
        self.product_repository: ProductRepositoryABC = product_repository

    def add_cart(self) -> CartSchema:
        with self.database.get_session() as session:

            cart: CartEntity = CartEntity(
                id=uuid.uuid4(),
                amount=0,
            )
            self.cart_repository.create_cart(session, cart)
            return EntityToSchemaMapper.getSchemaFromCartEntity(cart)

    def add_to_cart(self, product_id: uuid.UUID, cart_id: str, qty: int) -> CartSchema:
        # this block will ensure that all the db operations occurs in the same DB transaction
        with self.database.get_session() as session:
            product_entity: ProductEntity = self.product_repository.find_product_by_id(
                session, product_id
            )
            if product_entity:
                if (
                    product_entity.qty < qty
                ):  # check whether requested quantity is available
                    raise NotAvailableError(
                        f"Requested quantity [{qty}] not available. Available quantity: {product_entity.qty}"  # noqa E501
                    )

                cart_entity: CartEntity = OrderServiceHelper.add_to_cart(
                    session,
                    cart_id,
                    product_entity,
                    qty,
                    self.cart_repository,
                    self.cart_product_repository,
                    self.product_repository,
                )

                return EntityToSchemaMapper.getSchemaFromCartEntity(
                    self.cart_repository.get_cart(session, cart_entity.id)
                )
            else:
                raise NotFoundError(
                    f"Unable to add to cart due to product is not found for the product_id: {product_id}"  # noqa E501
                )

    def remove_from_cart(self, product_id: uuid.UUID, cart_id: uuid.UUID) -> CartSchema:
        with self.database.get_session() as session:
            cart_entity: CartEntity = self.cart_repository.get_cart(session, cart_id)

            for cart_product in cart_entity.cart_products[
                :
            ]:  # Work on a copy of the list
                if cart_product.product_id == product_id:
                    qty_in_cart: int = cart_product.qty
                    product_entity: ProductEntity = cart_product.product

                    # Update product stock on hand
                    product_entity.qty += qty_in_cart

                    # Update cart total amount
                    cart_entity.amount -= qty_in_cart * product_entity.price

                    cart_entity.cart_products.remove(
                        cart_product
                    )  # Remove cart_product_entity from the cart's products list. # noqa E501
                    session.delete(
                        cart_product
                    )  # Delete cart_product_entity from the database.

            return EntityToSchemaMapper.getSchemaFromCartEntity(cart_entity)

    def view_items_in_the_cart(self, cart_id: uuid.UUID) -> CartSchema:
        with self.database.get_session() as session:
            cart_entity: CartEntity = self.cart_repository.get_cart(session, cart_id)
            if not cart_entity:
                raise NotFoundError(f"No cart for cart id : {cart_id}")
            return EntityToSchemaMapper.getSchemaFromCartEntity(cart_entity)

    def checkout_order(
        self,
        cart_id: uuid.UUID,
        address: str,
        delivery_time: datetime,
    ) -> OrderSchema:
        with self.database.get_session() as session:
            cart_entity: CartEntity = self.cart_repository.get_cart(session, cart_id)
            if not cart_entity:
                raise NotFoundError(f"Unable to find cart for id: {cart_id}")

            order_entity: OrderEntity = OrderEntity(
                id=uuid.uuid4(),
                cart_id=cart_id,
                total_amount=cart_entity.amount,
                delivery_address=address,
                delivery_time=delivery_time,
                delivery_status="PENDING",
                cart_entity=cart_entity,
            )
            self.order_repository.add_order(session, order_entity)  # save order
            return EntityToSchemaMapper.getOrderSchemaFromOrderEntity(order_entity)

    def view_order(self, order_id: uuid.UUID) -> OrderSchema:
        with self.database.get_session() as session:
            order_entity: OrderEntity = self.order_repository.view_order_by_id(
                session, order_id
            )

            if not order_entity:
                raise NotFoundError(f"Order not found for the id: {order_id}")

            return EntityToSchemaMapper.getOrderSchemaFromOrderEntity(order_entity)
