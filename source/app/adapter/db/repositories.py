from typing import Optional, cast

from source.app.adapter.db.model.cart import SQLCartRepository
from source.app.adapter.db.model.cart_item import SQLCartItemRepository
from source.app.adapter.db.model.order import SQLOrderRepository
from source.app.adapter.db.model.product import SQLProductRepository
from source.app.adapter.db.model.user import SQLUserRepository
from source.app.ports.db import DbAdapter, Repositories

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

    @property
    def cart(self):
        return SQLCartRepository(self.db)

    @property
    def cart_item(self):
        return SQLCartItemRepository(self.db)

    @property
    def order(self):
        return SQLOrderRepository(self.db)
