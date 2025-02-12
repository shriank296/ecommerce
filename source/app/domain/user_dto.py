from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class BaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseUserDTO(BaseDto):
    first_name: str
    last_name: Optional[str] = None
    email: str
    phone: str
    address: dict
    role: str

class UserDTO(BaseUserDTO):
    user_id: UUID    
    created_at: datetime
    updated_at: datetime

class CreateUserDTO(BaseUserDTO):
    _passowrd: str



    
