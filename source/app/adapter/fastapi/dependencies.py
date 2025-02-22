from collections.abc import Generator

from source.app.ports.db import DbAdapter, Repository, Repositories
from source.app.adapter.db import SQLAlchemyAdapter, SQLRepositories

from source.app.config import DB_URL

def get_db() -> Generator[DbAdapter, None, None]:
    adapter = SQLAlchemyAdapter(DB_URL)
    with adapter.transaction():
        yield adapter

def get_repos() -> Generator[Repositories, None, None]:
    adapter = SQLAlchemyAdapter(DB_URL)
    with adapter.transaction():
        yield SQLRepositories(adapter)