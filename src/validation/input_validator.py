from datetime import datetime

from src.core.exception import InvalidRequestError
from src.schema import (
    CheckoutOrderRequest,
    CreateProductRequest,
    UpdateProductRequest,
)
from src.util.utils import is_valid_uuid


class RequestValidator:
    @staticmethod
    def validate_create_product_request(request: CreateProductRequest) -> None:
        if not request.name:
            raise InvalidRequestError("Product name is not present in the request")

        if request.price <= 0:
            raise InvalidRequestError("Product price should be greater than 0")

    @staticmethod
    def validate_update_product_request(request: UpdateProductRequest) -> None:
        if not request.product.name:
            raise InvalidRequestError("Product name is not present in the request")

        if request.product.price <= 0:
            raise InvalidRequestError("Product price should be greater than 0")

        if request.product.qty < 0:
            raise InvalidRequestError("Product quantity can be updated to minus value")

    @staticmethod
    def validate_add_to_cart_request(cart_id: str, product_id: str, qty: int) -> None:
        if not is_valid_uuid(product_id):
            raise InvalidRequestError(
                f"Invalid product id present in the request: {product_id}"
            )

        if not is_valid_uuid(cart_id):
            raise InvalidRequestError(
                f"Invalid cart id present in the request: {cart_id}"
            )

        if qty <= 0:
            raise InvalidRequestError("Quantity of product should be greater than 0")

    @staticmethod
    def validate_remove_from_cart_request(cart_id: str, product_id: str) -> None:
        if not is_valid_uuid(product_id):
            raise InvalidRequestError(
                f"Invalid product id present in the request: {product_id}"
            )

        if not is_valid_uuid(cart_id):
            raise InvalidRequestError(
                f"Invalid product id present in the request: {cart_id}"
            )

    @staticmethod
    def validate_checkout_order_request(
        request: CheckoutOrderRequest, cart_id: str
    ) -> None:
        if not is_valid_uuid(cart_id):
            raise InvalidRequestError(
                f"Invalid cart id present in the request: {request.cart_id}"
            )

        if not isinstance(request.delivery_time, datetime):
            raise InvalidRequestError(
                "Delivery time is not in accepted format. Please provide in '%Y-%m-%d %H:%M:%S.%f' format"  # noqal E501
            )

        if not request.delivery_address:
            raise InvalidRequestError("Delivery address must be provided")
