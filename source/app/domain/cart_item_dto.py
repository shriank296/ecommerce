from typing import List
from uuid import UUID

from pydantic import Field, computed_field

from source.app.domain.product_dto import BaseProductDto
from .base_dto import BaseDto

class BaseCartItemDto(BaseDto):
    product_id: UUID = Field(..., alias="productId")
    quantity: int = Field(..., alias="quantity")
    cart_id: UUID = Field(...,alias="cartId")

class CartItemDto(BaseCartItemDto):
    cart_item_id: UUID = Field(...,alias="id")

class CreateCartItemDto(BaseCartItemDto):
    """
    Create cart Dto
    """
class ViewCartItemDto(BaseDto):
    product: BaseProductDto
    quantity: int

    @computed_field
    @property
    def cost(self) -> float:
        return self.product.price * self.quantity


class ViewCartDto(BaseDto):
    items: List[ViewCartItemDto]

    @computed_field
    @property
    def total_cost(self) -> float:
        return sum(item.cost for item in self.items)
