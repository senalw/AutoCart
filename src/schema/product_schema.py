import uuid
from typing import List

from pydantic import BaseModel
from src.schema import Request, Response


class ProductSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str
    qty: int


class CreateProductRequest(Request):
    name: str
    qty: int
    price: float
    description: str


class CreateProductResponse(Response):
    product: ProductSchema


class ListProductResponse(Response):
    products: List[ProductSchema]
    next_page_token: str


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
