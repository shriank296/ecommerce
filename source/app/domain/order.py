from datetime import datetime
from uuid import UUID

from pydantic import Field

from .base_dto import BaseDto


class BaseOrderDto(BaseDto):
    user_id: UUID = Field(..., alias="userId")
    status: str = Field(..., alias="status")
    total_amount: float = Field(..., alias="totalAmount")
    shipping_address: dict = Field(..., alias="shippingAddress")
    placed_at: datetime = Field(..., alias="placedAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class OrderDto(BaseOrderDto):
    order_id: UUID = Field(..., alias="id")
