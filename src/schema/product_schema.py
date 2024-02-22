import uuid
from typing import List, Optional

from src.schema.base_schema import Request, Response
from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str
    qty: int


class CreateProductRequest(Request):
    id: uuid.UUID
    name: str
    qty: int
    price: float
    description: str


class CreateProductResponse(Response):
    product: ProductSchema


class ListProductResponse(Response):
    products: List[ProductSchema]


class GetProductRequest(Request):
    id: uuid.UUID


class GetProductResponse(Response):
    product: ProductSchema


class UpdateProductRequest(Request):
    product: ProductSchema


class UpdateProductResponse(Response):
    product: ProductSchema


class DeleteProductRequest(Request):
    id: uuid.UUID


class DeleteProductResponse(Response):
    pass
