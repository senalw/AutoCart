import uuid
from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query, status
from src.core.container import Container
from src.core.exception import NotFoundError, ValidationError
from src.domain.entity import ProductEntity
from src.mapper import EntityToSchemaMapper, SchemaToEntityMapper
from src.schema import (
    CreateProductRequest,
    CreateProductResponse,
    GetProductResponse,
    ListProductResponse,
    ProductSchema,
    UpdateProductRequest,
    UpdateProductResponse,
)
from src.service import ProductService
from src.util.utils import get_next_page_token, get_page_number, is_valid_uuid
from src.validation.input_validator import RequestValidator

router = APIRouter(prefix="/products")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ListProductResponse,
)
@inject
async def list_products(
    page_size: int = Query(  # noqa B008
        ..., description="The number of products per page"
    ),
    page_token: str = Query(  # noqa B008
        None, description="The token of the page requested"
    ),
    product_service: ProductService = Depends(  # noqa B008
        Provide[Container.product_service]
    ),
) -> ListProductResponse:
    page_number: int = get_page_number(page_token)
    total_products: int = product_service.get_total_products_count()
    products: List[ProductSchema] = product_service.list_products(
        page_number, page_size
    )
    next_page_token: str = get_next_page_token(page_number, page_size, total_products)
    return ListProductResponse(products=products, next_page_token=next_page_token)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateProductResponse,
)
@inject
async def create_product(
    request: CreateProductRequest,
    product_service: ProductService = Depends(  # noqa B008
        Provide[Container.product_service]
    ),
) -> CreateProductResponse:

    RequestValidator.validate_create_product_request(request)
    product_entity: ProductEntity = SchemaToEntityMapper.getProductSchemaFromRequest(
        request, uuid.uuid4()
    )
    product_service.add_product(product_entity)

    return CreateProductResponse(
        product=EntityToSchemaMapper.getSchemaFromProductEntity(product_entity)
    )


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetProductResponse,
)
@inject
async def get_product_by_id(
    product_id: str,
    product_service: ProductService = Depends(  # noqa B008
        Provide[Container.product_service]
    ),
) -> GetProductResponse:
    product: Optional[ProductSchema] = product_service.get_product_by_id(  # noqa B008
        uuid.UUID(product_id)
    )
    if not product:
        raise NotFoundError(f"Product not found for the product_id: {product_id}")
    return GetProductResponse(product=product)


@router.put(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UpdateProductResponse,
)
@inject
async def update_product_by_id(
    request: UpdateProductRequest,
    product_service: ProductService = Depends(  # noqa B008
        Provide[Container.product_service]
    ),
) -> UpdateProductResponse:
    RequestValidator.validate_update_product_request(request)
    product: Optional[ProductSchema] = product_service.get_product_by_id(  # noqa B008
        request.product.product_id
    )
    if not product:
        raise NotFoundError(
            f"Product not found for the product_id: {request.product.product_id}"
        )

    updated_product: ProductSchema = product_service.update_product(
        SchemaToEntityMapper.getProductEntityFromSchema(request.product)
    )
    return UpdateProductResponse(product=updated_product)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_product_by_id(
    product_id: str,
    product_service: ProductService = Depends(  # noqa B008
        Provide[Container.product_service]
    ),
) -> None:
    if not is_valid_uuid(product_id):
        raise ValidationError(
            f"Invalid product id present in the request: {product_id}"
        )
    product_service.delete_product(uuid.UUID(product_id))
