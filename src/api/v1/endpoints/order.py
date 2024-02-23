import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from src.core.container import Container
from src.core.exception import RequestValidationError
from src.schema import (
    CheckoutOrderRequest,
    CheckoutOrderResponse,
    OrderSchema,
    ViewOrderResponse,
)
from src.service import OrderService
from src.util.utils import is_valid_uuid
from src.validation.input_validator import RequestValidator

router = APIRouter(prefix="/order")


@router.post(
    "/cart/{cart_id}",
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
    RequestValidator.validate_checkout_order_request(request, cart_id)
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
    if not is_valid_uuid(order_id):
        raise RequestValidationError("Invalid order_id present in the request")
    order_schema: OrderSchema = order_service.view_order(uuid.UUID(order_id))
    return ViewOrderResponse(order=order_schema)
