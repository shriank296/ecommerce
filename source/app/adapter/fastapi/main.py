from fastapi import FastAPI

from source.app.adapter.fastapi.exception_handlers import (
    db_error,
    empty_cart,
    not_enough_stock_handler,
)
from source.app.adapter.fastapi.routes.api import api_router
from source.app.adapter.logging_config import setup_logging
from source.app.domain.exception import DbException, EmptyCart, NotEnoughStock

setup_logging()

app = FastAPI(title="Ecommerce app")

app.add_exception_handler(NotEnoughStock, not_enough_stock_handler)
app.add_exception_handler(EmptyCart, empty_cart)
app.add_exception_handler(DbException, db_error)


app.include_router(api_router)


@app.get("/")
def hello():
    return {"message": "hello ecommerce"}
