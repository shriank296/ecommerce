import logging
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from source.app.adapter.db.model.order_item import OrderItem
from source.app.domain.exception import DbException, EmptyCart
from source.app.domain.order import BaseOrderDto
from source.app.ports.db.repositories import Repositories

logger = logging.getLogger(__name__)


def order_items(username: str, repos: Repositories):
    try:
        items = (
            repos.db.session.query(
                repos.cart_item.model.product_id,
                repos.cart_item.model.quantity,
                repos.product.model.price,
                repos.user.model.address,
                repos.user.model.id,
                repos.cart_item.model.id,
            )
            .filter(repos.user.model.id == repos.cart.model.user_id)
            .filter(repos.cart.model.id == repos.cart_item.model.cart_id)
            .filter(repos.product.model.id == repos.cart_item.model.product_id)
            .filter(repos.user.model.email == username)
            .all()
        )

        if items:
            order_obj = BaseOrderDto(
                user_id=items[0][4],
                status="PENDING",
                total_amount=sum(item[1] * item[2] for item in items),
                shipping_address=items[0][3],
                placed_at=datetime.now(),
                updated_at=datetime.now(),
            )
            order = repos.order.create(order_obj)
            for item in items:
                repos.db.session.add(
                    OrderItem(
                        order_id=order.order_id,
                        product_id=item[0],
                        quantity=item[1],
                        price=item[2],
                        total=item[1] * item[2],
                    )
                )
                repos.cart_item.delete(id=item[5])
        else:
            logger.error("Cart is empty")
            raise EmptyCart()
    except SQLAlchemyError as e:
        # rollback for session.add OrderItem and delete as create already has a rollback defined.
        repos.db.rollback()
        raise DbException(detail=str(e))
