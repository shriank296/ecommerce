from abc import ABC
from typing import Optional

from .adapter import DbAdapter


class Repositories(ABC):
    def __init__(self, db: Optional[DbAdapter]):
        self.db: Optional[DbAdapter] = db

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    @property
    def user(self):
        raise NotImplementedError

    @property
    def product(self):
        return NotImplementedError

    @property
    def cart(self):
        return NotImplementedError

    @property
    def cart_item(self):
        return NotImplementedError

    @property
    def order(self):
        return NotImplementedError
