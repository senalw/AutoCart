import uuid
from typing import List, Optional

from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import func
from src.domain.entity import ProductEntity
from src.repository.product_repository import ProductRepositoryABC


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
        page_numer: int,
        page_size: int,
    ) -> List[ProductEntity]:
        query: Query = session.query(ProductEntity)
        query = query.limit(limit=page_size).offset(page_numer)
        return query.all()

    def update(
        self, session: Session, product: ProductEntity
    ) -> Optional[ProductEntity]:
        pass

    def delete_product_by_id(self, session: Session, product_id: uuid.UUID) -> int:
        return (
            session.query(ProductEntity).filter(ProductEntity.id == product_id).delete()
        )

    def get_total_products_count(self, session: Session) -> int:
        # Just returning count without fetching all the columns
        return (
            session.query(ProductEntity)
            .with_entities(func.count(ProductEntity.id))
            .scalar()
        )
