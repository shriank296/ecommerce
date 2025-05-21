from __future__ import annotations

from abc import ABC
from typing import Any, Optional, TypeVar

from pydantic import BaseModel

from .adapter import DbAdapter

ModelDTO = TypeVar("ModelDTO", bound=BaseModel)


class PaginatedData(BaseModel):
    results: Any = (None,)
    total: int = 0
    page_size: int = 100
    page_number: int = 1


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
