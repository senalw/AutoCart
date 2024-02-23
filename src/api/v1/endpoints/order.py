import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from src.core.container import Container
from src.schema import (
    CheckoutOrderRequest,
    CheckoutOrderResponse,
    OrderSchema,
    ViewOrderResponse,
)
from src.service import OrderService

router = APIRouter(prefix="/order")


@router.post(
    "/checkout/{cart_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=CheckoutOrderResponse,
)
@inject
async def checkout_order(
    cart_id: str,
    request: CheckoutOrderRequest,
    order_service: OrderService = Depends(  # noqa B008
        Provide[Container.order_service]
    ),
) -> CheckoutOrderResponse:
    order_schema: OrderSchema = order_service.checkout_order(
        uuid.UUID(cart_id),
        request.delivery_address,
        request.delivery_time,
    )
    return CheckoutOrderResponse(order=order_schema)


@router.get(
    "/{order_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ViewOrderResponse,
)
@inject
async def view_order(
    order_id: str,
    order_service: OrderService = Depends(  # noqa B008
        Provide[Container.order_service]
    ),
) -> ViewOrderResponse:
    order_schema: OrderSchema = order_service.view_order(uuid.UUID(order_id))
    return ViewOrderResponse(order=order_schema)
