import uuid
from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from src.core.container import Container
from src.core.exception import NotFoundError
from src.domain.entity import ProductEntity
from src.mapper import SchemaToEntityMapper
from src.schema import (
    CreateProductRequest,
    CreateProductResponse,
    DeleteProductResponse,
    GetProductResponse,
    ListProductResponse,
    ProductSchema,
    UpdateProductRequest,
    UpdateProductResponse,
)
from src.service import ProductService

router = APIRouter(prefix="/product")


@router.get(
    "/list-products", status_code=status.HTTP_200_OK, response_model=ListProductResponse
)
@inject
async def list_products(
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> ListProductResponse:
    products: List[ProductSchema] = product_service.list_products()
    return ListProductResponse(products=products)


@router.post(
    "/add-product",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateProductResponse,
)
@inject
async def create_product(
    request: CreateProductRequest,
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> CreateProductResponse:

    # If product_id is not provided, it'll be generated internally
    product_id: uuid.UUID = request.id if request.id else uuid.uuid4()

    product_entity: ProductEntity = ProductEntity(
        id=product_id,
        name=request.name,
        price=request.price,
        description=request.description,
        qty=request.qty,
    )
    product_service.add_product(product_entity)

    return CreateProductResponse(
        product=ProductSchema(
            id=product_id,
            name=request.name,
            price=request.price,
            description=request.description,
            qty=request.qty,
        )
    )


@router.get(
    "/get/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetProductResponse,
)
@inject
async def get_product_by_id(
    product_id: str,
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> GetProductResponse:
    product: Optional[ProductSchema] = product_service.get_product_by_id(
        uuid.UUID(product_id)
    )
    if not product:
        raise NotFoundError(f"Product not found for the product_id: {product_id}")
    return GetProductResponse(product=product)


@router.put(
    "/update-product",
    status_code=status.HTTP_200_OK,
    response_model=UpdateProductResponse,
)
@inject
async def get_product_by_id(
    request: UpdateProductRequest,
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> UpdateProductResponse:
    product_id = request.product.id
    product: Optional[ProductSchema] = product_service.get_product_by_id(product_id)
    if not product:
        raise NotFoundError(f"Product not found for the product_id: {product_id}")

    updated_product: ProductSchema = product_service.update_product(
        SchemaToEntityMapper.getProductEntityFromSchema(request.product)
    )
    return UpdateProductResponse(product=updated_product)


@router.delete(
    "/delete/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteProductResponse,
)
@inject
async def delete_product_by_id(
    product_id: str,
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> DeleteProductResponse:
    product_service.delete_product(uuid.UUID(product_id))
    return DeleteProductResponse()
