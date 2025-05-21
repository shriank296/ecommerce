from fastapi import Request
from fastapi.responses import JSONResponse

from source.app.domain.exception import DbException, EmptyCart, NotEnoughStock


def not_enough_stock_handler(request: Request, exc: NotEnoughStock):
    return JSONResponse(
        status_code=409,
        content={
            "detail": f"Not enough stock for product {exc.product_id}. Available: {exc.available_quantity}"
        },
    )


def empty_cart(request: Request, exc: EmptyCart):
    return JSONResponse(status_code=400, content={"detail": "Your cart is empty"})


def db_error(request: Request, exc: DbException):
    return JSONResponse(
        status_code=500, content={"detail": "Unexpected db error occured"}
    )
