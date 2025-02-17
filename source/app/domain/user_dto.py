from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class BaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True, allow_population_by_field_name = True, orm_mode = True)

class BaseUserDTO(BaseDto):
    first_name: str
    last_name: Optional[str] = None
    email: str
    phone: str
    address: dict
    role: str

class UserDTO(BaseUserDTO):
    user_id: UUID = Field(..., alias='id')
    created_at: datetime
    updated_at: datetime

class CreateUserDTO(BaseUserDTO):
    password: str



    
