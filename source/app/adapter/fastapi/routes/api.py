from fastapi import APIRouter

from .auth import router as login_router
from .cart_item import router_v1 as cart_item_router
from .order import router_v1 as place_order_router
from .product import router_v1 as product_router
from .user import router_v1 as user_router

api_router = APIRouter()

api_router.include_router(user_router, tags=["Users"], prefix="/users")
api_router.include_router(product_router, tags=["Products"], prefix="/products")
api_router.include_router(login_router, prefix="/login")
api_router.include_router(cart_item_router, prefix="/cart_item")
api_router.include_router(place_order_router, tags=["Orders"])
