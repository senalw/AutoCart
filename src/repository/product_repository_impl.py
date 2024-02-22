import uuid
from typing import Any, List, Optional

from src.domain.entity import ProductEntity
from src.repository.product_repository import ProductRepositoryABC
from sqlalchemy.orm import Session, Query


class ProductRepositoryImpl(ProductRepositoryABC):
    def add_product(self, session: Session, product: ProductEntity) -> None:
        session.add(product)

    def find_product_by_id(
        self, session: Session, product_id: uuid.UUID
    ) -> Optional[ProductEntity]:
        query: Query = session.query(ProductEntity).filter(
            ProductEntity.id == product_id
        )
        return query.first()

    def fetch_products(
        self,
        session: Session,
    ) -> List[ProductEntity]:
        query: Query = session.query(ProductEntity)
        return query.all()

    def update(
        self, session: Session, product: ProductEntity
    ) -> Optional[ProductEntity]:
        pass

    def delete_product_by_id(self, session: Session, product_id: uuid.UUID) -> int:
        return (
            session.query(ProductEntity).filter(ProductEntity.id == product_id).delete()
        )

    def get_selected_columns(
        self, session: Session, product_id: uuid.UUID, fields: List[Any]
    ) -> Optional[ProductEntity]:
        query: Query = session.query(*fields).filter(ProductEntity.id == product_id)
        return query.first()
