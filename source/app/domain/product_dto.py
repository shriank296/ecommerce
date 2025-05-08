from pydantic import Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from source.app.domain.category_dto import CategoryDto
from .base_dto import BaseDto

class BaseProductDto(BaseDto):
    name: str = Field(..., alias="name")
    description: str = Field(...,alias="description")
    price: float = Field(...,alias="price")
    

class ProductDto(BaseProductDto):
    product_id: UUID = Field(...,alias="id")
    stock: int = Field(...,alias="stock")
    category_id: Optional[UUID] = Field(alias="categoryId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

class CreateProductDto(BaseProductDto):
    pass