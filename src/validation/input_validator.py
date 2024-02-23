from datetime import datetime

from src.core.exception import ValidationError
from src.schema import (
    AddToCartRequest,
    CheckoutOrderRequest,
    CreateProductRequest,
    RemoveFromCartRequest,
    UpdateProductRequest,
)
from src.util.utils import is_valid_uuid


class RequestValidator:
    @staticmethod
    def validate_create_product_request(request: CreateProductRequest) -> None:
        if not request.name:
            raise ValidationError("Product name is not present in the request")

        if not request.price <= 0:
            raise ValidationError("Product price should be greater than 0")

    @staticmethod
    def validate_update_product_request(request: UpdateProductRequest) -> None:
        if not request.product.name:
            raise ValidationError("Product name is not present in the request")

        if not request.product.price <= 0:
            raise ValidationError("Product price should be greater than 0")

        if not request.product.qty < 0:
            raise ValidationError("Product quantity can be updated to minus value")

    @staticmethod
    def validate_add_to_cart_request(
        request: AddToCartRequest, product_id: str
    ) -> None:
        if not is_valid_uuid(product_id):
            raise ValidationError(
                f"Invalid product id present in the request: {request.product_id}"
            )

        if not is_valid_uuid(request.cart_id):
            raise ValidationError(
                f"Invalid cart id present in the request: {request.cart_id}"
            )

        if not request.qty <= 0:
            raise ValidationError("Quantity of product should be greater than 0")

    @staticmethod
    def validate_remove_from_cart_request(
        request: RemoveFromCartRequest, product_id: str
    ) -> None:
        if not is_valid_uuid(product_id):
            raise ValidationError(
                f"Invalid product id present in the request: {product_id}"
            )

        if not is_valid_uuid(str(request.cart_id)):
            raise ValidationError(
                f"Invalid product id present in the request: {request.cart_id}"
            )

    @staticmethod
    def validate_checkout_order_request(
        request: CheckoutOrderRequest, cart_id: str
    ) -> None:
        if not is_valid_uuid(cart_id):
            raise ValidationError(
                f"Invalid cart id present in the request: {request.cart_id}"
            )

        if not isinstance(request.delivery_time, datetime):
            raise ValidationError(
                "Delivery time is not in accepted format. Please provide in '%Y-%m-%d %H:%M:%S.%f' format"  # noqal E501
            )

        if not request.delivery_address:
            raise ValidationError("Delivery address must be provided")
