from .base_dto import BaseDto
from uuid import UUID
from pydantic import Field

class BaseCategoryDto(BaseDto):
    name: str = Field(..., alias="name")


class CategoryDto(BaseCategoryDto):
    category_id: UUID = Field(...,alias="Id")