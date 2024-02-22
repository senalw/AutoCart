import uuid
from typing import List, Optional

from src.core.database.postgres_client import PostgresClient
from src.domain.entity import ProductEntity
from src.mapper import EntityToSchemaMapper
from src.repository import ProductRepositoryABC
from src.schema.product_schema import ProductSchema


class ProductService:
    def __init__(
        self, database: PostgresClient, product_repository: ProductRepositoryABC
    ) -> None:
        self.database: PostgresClient = database
        self.product_repository: ProductRepositoryABC = product_repository

    def list_products(self) -> List[ProductSchema]:
        products: List[ProductSchema] = []
        with self.database.get_session() as session:
            for product_entity in self.product_repository.fetch_products(session):
                products.append(
                    EntityToSchemaMapper.getSchemaFromProductEntity(product_entity)
                )
        return products

    def add_product(self, product: ProductEntity) -> None:
        with self.database.get_session() as session:
            self.product_repository.add_product(session, product)

    def get_product_by_id(self, product_id: uuid.UUID) -> Optional[ProductSchema]:
        with self.database.get_session() as session:
            product_entity: Optional[
                ProductEntity
            ] = self.product_repository.find_product_by_id(session, product_id)
            if product_entity:
                return EntityToSchemaMapper.getSchemaFromProductEntity(product_entity)

    def update_product(self, product: ProductEntity) -> ProductSchema:
        with self.database.get_session() as session:
            product_entity: ProductEntity = session.merge(product)
            return EntityToSchemaMapper.getSchemaFromProductEntity(product_entity)

    def delete_product(self, product_id: uuid.UUID) -> int:
        with self.database.get_session() as session:
            return self.product_repository.delete_product_by_id(session, product_id)
