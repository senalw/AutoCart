import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session
from src.domain.entity import ProductEntity


class ProductRepositoryABC(ABC):
    @abstractmethod
    def add_product(self, session: Session, product: ProductEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_product_by_id(
        self, session: Session, product_id: uuid.UUID
    ) -> Optional[ProductEntity]:
        raise NotImplementedError

    @abstractmethod
    def fetch_products(
        self,
        session: Session,
        page_numer: int,
        page_size: int,
    ) -> List[ProductEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(
        self, session: Session, product: ProductEntity
    ) -> Optional[ProductEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_product_by_id(self, session: Session, product_id: uuid.UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_total_products_count(self, session: Session) -> int:
        raise NotImplementedError
