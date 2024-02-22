import uuid
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from src.domain.entity import ProductEntity
from sqlalchemy.orm import Session


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
    def get_selected_columns(
        self, session: Session, product_id: uuid.UUID, fields: List[Any]
    ) -> Optional[ProductEntity]:
        raise NotImplementedError
