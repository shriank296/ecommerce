from uuid import UUID

from pydantic import Field
from .base_dto import BaseDto
from .product_dto import BaseProductDto

class BaseCartDto(BaseDto):
    user_id: UUID = Field(..., alias="UserId")

class CartDto(BaseCartDto):
    cart_id: UUID = Field(...,alias="id")

class CreateCartDto(BaseCartDto):
    pass        