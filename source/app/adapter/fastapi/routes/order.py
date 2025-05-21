import logging

from fastapi import Depends

from source.app.adapter.fastapi.crud import CrudRouter
from source.app.adapter.fastapi.dependencies import get_repos
from source.app.adapter.token.oauth2 import check_roles
from source.app.domain.exception import DbException
from source.app.domain.order import BaseOrderDto, OrderDto
from source.app.domain.place_order import order_items

logger = logging.getLogger(__name__)

router_v1 = CrudRouter(
    repo_dependency=get_repos,
    role_dependency=check_roles,
    repository="order",
    methods_and_roles={},
    response_schema=OrderDto,
    create_schema=BaseOrderDto,
    update_schema=OrderDto,
)


@router_v1.post("/place_order")
def order(repos=Depends(get_repos), user=Depends(check_roles(["customer", "admin"]))):
    try:
        order = order_items(user.get("username"), repos)
    except DbException as e:
        logger.error(f"Database exception occurred: {e.detail}")
        raise
    return {"success": "Order placed"}
