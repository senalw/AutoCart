from typing import List

from src.domain.entity import CartEntity, OrderEntity, ProductEntity
from src.schema import CartSchema, OrderSchema, ProductSchema


class EntityToSchemaMapper:
    @staticmethod
    def getSchemaFromProductEntity(product_entity: ProductEntity) -> ProductSchema:
        return ProductSchema(
            id=product_entity.id,
            name=product_entity.name,
            price=product_entity.price,
            description=product_entity.description,
            qty=product_entity.qty,
        )

    @staticmethod
    def getSchemaFromCartEntity(cart_entity: CartEntity) -> CartSchema:
        return CartSchema(
            cart_id=cart_entity.id,
            products=EntityToSchemaMapper._get_product_schema_from_cart_entity(
                cart_entity
            ),
            amount=cart_entity.amount,
        )

    @staticmethod
    def getOrderSchemaFromOrderEntity(
        order_entity: OrderEntity,
    ) -> OrderSchema:
        return OrderSchema(
            order_id=order_entity.id,
            cart_id=order_entity.cart_id,
            total_amount=order_entity.total_amount,
            delivery_address=order_entity.delivery_address,
            delivery_time=order_entity.delivery_time,
            delivery_status=order_entity.delivery_status,
            items=EntityToSchemaMapper._get_product_schema_from_cart_entity(
                order_entity.cart_entity
            ),
        )

    @staticmethod
    def _get_product_schema_from_cart_entity(
        cart_entity: CartEntity,
    ) -> List[ProductSchema]:
        products_schema: List[ProductSchema] = []
        for cart_product in cart_entity.cart_products:
            products_schema.append(
                ProductSchema(
                    id=cart_product.product.id,
                    name=cart_product.product.name,
                    price=cart_product.product.price,
                    description=cart_product.product.description,
                    qty=cart_product.qty,
                )
            )
        return products_schema
