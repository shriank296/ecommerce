from collections.abc import Generator

from source.app.adapter.token.jwt_token import JWTTokenService
from source.app.ports.db import DbAdapter, Repository, Repositories
from source.app.adapter.db import SQLAlchemyAdapter, SQLRepositories

from source.app.config import DB_URL, SECRET_KEY

ALGORITHM = "HS256"

def get_db() -> Generator[DbAdapter, None, None]:
    adapter = SQLAlchemyAdapter(DB_URL)
    with adapter.transaction():
        yield adapter

def get_repos() -> Generator[Repositories, None, None]:
    adapter = SQLAlchemyAdapter(DB_URL)
    with adapter.transaction():
        yield SQLRepositories(adapter)

def get_token_service():
    return JWTTokenService(secret_key=SECRET_KEY, algorithm=ALGORITHM)