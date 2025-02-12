from __future__ import annotations
from abc import ABC

from .adapter import DbAdapter
from typing import Optional, List, TypeVar, Any

from pydantic import BaseModel

ModelDTO = TypeVar("ModelDTO", bound=BaseModel)

class Repository(ABC):
    def __init__(self, db: Optional[DbAdapter] = None):
        self.db = db

    def create(self, obj_in: Any) -> Any:
        raise NotImplementedError
    
    def read(self, id: Any, **kwargs):
        raise NotImplementedError
    
    def update(self, obj_in: Any) -> Any:
        raise NotImplementedError
    
    def delete(self, id: Any) -> bool:
        raise NotImplementedError

        
