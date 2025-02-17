from fastapi import APIRouter
from .user import router_v1 as user_router

api_router = APIRouter()

api_router.include_router(user_router, tags=["Users"], prefix="/users")