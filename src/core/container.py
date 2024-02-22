from dependency_injector import containers, providers
from src.config.config import Config
from src.core.database.postgres_client import PostgresClient
from src.repository import (
    CartProductRepositoryImpl,
    CartRepositoryImpl,
    OrderRepositoryImpl,
    ProductRepositoryImpl,
)
from src.service import OrderService, ProductService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.product",
            "src.api.v1.endpoints.cart",
            "src.api.v1.endpoints.order",
        ]
    )

    conf: Config = Config.get_instance()
    db = providers.Singleton(PostgresClient, configs=conf.db_configs)

    product_repository = providers.Factory(ProductRepositoryImpl)
    cart_repository = providers.Factory(CartRepositoryImpl)
    cart_product_repository = providers.Factory(CartProductRepositoryImpl)
    order_repository = providers.Factory(OrderRepositoryImpl)

    product_service = providers.Factory(
        ProductService, database=db, product_repository=product_repository
    )

    order_service = providers.Factory(
        OrderService,
        database=db,
        cart_repository=cart_repository,
        cart_product_repository=cart_product_repository,
        order_repository=order_repository,
        product_repository=product_repository,
    )
