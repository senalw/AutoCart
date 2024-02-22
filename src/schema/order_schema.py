import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel
from src.schema import Request, Response
from src.schema.product_schema import ProductSchema


class OrderSchema(BaseModel):
    order_id: uuid.UUID
    cart_id: uuid.UUID
    total_amount: float
    delivery_address: str
    delivery_time: datetime
    delivery_status: str
    items: List[ProductSchema]


class CheckoutOrderRequest(Request):
    delivery_address: str
    delivery_time: datetime


class CheckoutOrderResponse(Response):
    order: OrderSchema


class ViewOrderResponse(Response):
    order: OrderSchema
