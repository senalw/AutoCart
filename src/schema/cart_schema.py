import uuid
from typing import List

from pydantic import BaseModel
from src.schema import Request, Response
from src.schema.product_schema import ProductSchema


class CartSchema(BaseModel):
    cart_id: uuid.UUID
    products: List[ProductSchema]
    amount: float


class CreateCartResponse(Response):
    cart_id: uuid.UUID


class AddToCartResponse(Response):
    items: CartSchema


class ViewCartItemsRequest(Request):
    cart_id: uuid.UUID


class ViewCartItemsResponse(Response):
    items: CartSchema
