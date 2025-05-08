from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from source.app.domain.exception import EmptyCart, NotEnoughStock

async def not_enough_stock_handler(request: Request, exc: NotEnoughStock):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Not enough stock for product {exc.product_id}. Available: {exc.available_quantity}"}
    )

async def empty_cart(request: Request, exc: EmptyCart):
    return JSONResponse(
        status_code=204,
        detail = {"Your cart is empty, please add some items"}
    )