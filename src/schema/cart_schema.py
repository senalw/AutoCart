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


class AddToCartRequest(Request):
    # If cart_id is not in the request, then api generates a new UUID for the cart and creates a new cart. # noqa E501
    cart_id: str
    qty: int


class AddToCartResponse(Response):
    items: CartSchema


class RemoveFromCartRequest(Request):
    # If cart_id is not in the request, then api generates a new UUID for the cart and creates a new cart. # noqa E501
    cart_id: uuid.UUID


class RemoveFromCartResponse(Response):
    pass


class ViewCartItemsRequest(Request):
    # If cart_id is not in the request, then api generates a new UUID for the cart and creates a new cart. # noqa E501
    cart_id: uuid.UUID


class ViewCartItemsResponse(Response):
    items: CartSchema
