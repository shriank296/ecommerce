from uuid import UUID

from fastapi import Depends, HTTPException
from source.app.adapter.fastapi.crud import CrudRouter
from source.app.adapter.fastapi.dependencies import get_repos
from source.app.adapter.token.oauth2 import check_roles, get_current_user
from source.app.domain.view_cart import view_cart
from source.app.domain.add_cart import add_to_cart
from source.app.domain.cart_item_dto import CartItemDto, CreateCartItemDto
from source.app.domain.exception import DbException, NotEnoughStock



router_v1 = CrudRouter(
    repo_dependency=get_repos,
    role_dependency=check_roles,
    repository="product",
    methods_and_roles={},
    response_schema=CartItemDto,
    create_schema=CreateCartItemDto,
    update_schema=CartItemDto
)

@router_v1.post("/add_items")
def add_item(
    product_id: UUID,
    quantity: int,
    repos = Depends(get_repos),
    user = Depends(check_roles(["customer","admin"]))
):
    try:
        cart_item = add_to_cart(user.get("username"), product_id, quantity, repos)
    except NotEnoughStock as e:
        raise HTTPException(status_code=409, detail=str(e))    
    except DbException:
        raise HTTPException(status_code=500, detail="An Unexpected database exception occured")
    return cart_item

@router_v1.get("/view_items")
def get_items(
    repos = Depends(get_repos),
    user = Depends(check_roles(["customer", "admin"]))
):
    try:
        all_products = view_cart(user.get("username"), repos)
    except DbException:
        raise HTTPException(status_code=500, detail="An Unexpected database exception occured")   
    return all_products