from typing import Optional, cast

from app.ports.db import DbAdapter, Repository, Repositories
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
        

