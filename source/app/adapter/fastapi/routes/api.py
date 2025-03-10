from fastapi import APIRouter
from .user import router_v1 as user_router
from .product import router_v1 as product_router
from .auth import router as login_router
api_router = APIRouter()

api_router.include_router(user_router, tags=["Users"], prefix="/users")
api_router.include_router(product_router, tags=["Products"], prefix = "/products")
api_router.include_router(login_router, prefix = "/login")