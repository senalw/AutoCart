from src.domain.entity import ProductEntity, OrderEntity
from src.schema import OrderSchema
from src.schema.product_schema import ProductSchema


class SchemaToEntityMapper:
    @staticmethod
    def getProductEntityFromSchema(product_schema: ProductSchema) -> ProductEntity:
        return ProductEntity(
            id=product_schema.id,
            name=product_schema.name,
            price=product_schema.price,
            description=product_schema.description,
            qty=product_schema.qty,
        )

    @staticmethod
    def getOrderSchemaFromEntity(order_schema: OrderSchema) -> OrderEntity:
        return OrderEntity(
            id=order_schema.order_id,
            user_id=order_schema.user_id,
            total_amount=order_schema.total_amount,
            delivery_address=order_schema.delivery_address,
            delivery_time=order_schema.delivery_time,
            delivery_status=order_schema.delivery_status,
            items=order_schema.items,
        )
