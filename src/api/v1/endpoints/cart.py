import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query, status
from src.core.container import Container
from src.core.exception import RequestValidationError
from src.schema import (
    AddToCartResponse,
    CartSchema,
    CreateCartResponse,
    ViewCartItemsResponse,
)
from src.service import OrderService
from src.util.utils import is_valid_uuid
from src.validation.input_validator import RequestValidator

router = APIRouter(prefix="/cart")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateCartResponse,
)
@inject
async def create_cart(
    order_service: OrderService = Depends(  # noqa B008
        Provide[Container.order_service]
    ),
) -> CreateCartResponse:
    cart_schema: CartSchema = order_service.add_cart()
    return CreateCartResponse(
        cart_id=cart_schema.cart_id,
    )


@router.post(
    "/{cart_id}/product/{product_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=AddToCartResponse,
)
@inject
async def add_to_cart(
    cart_id: str,
    product_id: str,
    qty: int = Query(  # Default value of 1 if qty is not provided. # noqa B008
        default=1, gt=0
    ),
    order_service: OrderService = Depends(  # noqa B008
        Provide[Container.order_service]
    ),
) -> AddToCartResponse:
    RequestValidator.validate_add_to_cart_request(cart_id, product_id, qty)
    cart_schema: CartSchema = order_service.add_to_cart(
        uuid.UUID(product_id), uuid.UUID(cart_id), qty
    )
    return AddToCartResponse(items=cart_schema)


@router.delete(
    "/{cart_id}/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def remove_item_from_cart(
    cart_id: str,
    product_id: str,
    order_service: OrderService = Depends(  # noqa B008
        Provide[Container.order_service]
    ),
) -> None:
    RequestValidator.validate_remove_from_cart_request(cart_id, product_id)
    order_service.remove_from_cart(uuid.UUID(product_id), uuid.UUID(cart_id))


@router.get(
    "/{cart_id}",
    status_code=status.HTTP_200_OK,
    response_model=ViewCartItemsResponse,
)
@inject
async def view_cart_items(
    cart_id: str,
    order_service: OrderService = Depends(  # noqa B008
        Provide[Container.order_service]
    ),
) -> ViewCartItemsResponse:
    if not is_valid_uuid(cart_id):
        raise RequestValidationError(
            f"Invalid cart id present in the request: {cart_id}"
        )
    items: CartSchema = order_service.view_items_in_the_cart(uuid.UUID(cart_id))
    return ViewCartItemsResponse(items=items)
