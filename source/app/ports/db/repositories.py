from abc import ABC
from .adapter import DbAdapter
from .repository import Repository
from typing import Optional

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

