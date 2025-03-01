from typing import Optional, cast

from source.app.adapter.db.model.product import SQLProductRepository
from source.app.ports.db import DbAdapter, Repository, Repositories
from source.app.adapter.db.model.user import SQLUserRepository
from .sqlalchemy import SQLAlchemyAdapter

class SQLRepositories(Repositories):
    def __init__(self, db: Optional[DbAdapter] = None):
        super().__init__(db)
        assert self.db
        self.db: SQLAlchemyAdapter = cast(SQLAlchemyAdapter, db)

    def commit(self):
        self.db.session.commit()

    def rollback(self):
        self.db.session.rollback()

    @property
    def user(self):
        return SQLUserRepository(self.db)         
    
    @property
    def product(self):
        return SQLProductRepository(self.db)
        

