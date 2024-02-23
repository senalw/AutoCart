from fastapi import APIRouter
from src.api.v1.endpoints.cart import router as cart_router
from src.api.v1.endpoints.order import router as order_router
from src.api.v1.endpoints.product import router as product_router

routers = APIRouter()
router_list = [product_router, cart_router, order_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
