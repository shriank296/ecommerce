from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_dto import BaseDto


class BaseUserDTO(BaseDto):
    first_name: str
    last_name: Optional[str] = None
    email: str
    phone: str
    address: dict
    role: str


class UserDTO(BaseUserDTO):
    user_id: UUID = Field(..., alias="id")
    created_at: datetime
    updated_at: datetime


class CreateUserDTO(BaseUserDTO):
    password: str
