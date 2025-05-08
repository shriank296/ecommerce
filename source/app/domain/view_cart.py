from source.app.domain.cart_item_dto import ViewCartDto, ViewCartItemDto
from source.app.domain.exception import DbException, EmptyCart
from source.app.domain.product_dto import BaseProductDto
from source.app.ports.db.repositories import Repositories


# def view_cart(username: str, repos: Repositories):
#     try:
#         user_id = repos.db.session.query(repos.user.model.id).filter(repos.user.model.email == username).scalar()
#         cart_id = repos.db.session.query(repos.cart.model.id).filter(repos.cart.model.user_id == user_id).scalar()
#         if not cart_id:
#             raise EmptyCart()
#         cart_items = repos.db.session.query(repos.cart_item.model.product_id, repos.cart_item.model.quantity).filter(repos.cart_item.model.cart_id == cart_id).all()

#         all_products = repos.db.session.query(repos.product.model).filter(repos.product.model.id.in_(cart_item[0] for cart_item in cart_items)).all()

#         items = [ViewCartItemDto(product=product, quantity=cart_item[1]) for product, cart_item in zip(all_products, cart_items)]
#         # breakpoint()
#     except DbException:
#         raise
#     return ViewCartDto(items=items)


def view_cart(username: str, repos: Repositories):
    try:
        values = repos.db.session.query(
            repos.product.model.name,
            repos.product.model.description,
            repos.product.model.price,
            repos.cart_item.model.quantity,
        ).filter(
            repos.user.model.id == repos.cart.model.user_id
        ).filter(
            repos.cart.model.id == repos.cart_item.model.cart_id
        ).filter(
            repos.cart_item.model.product_id == repos.product.model.id
        ).filter(
            repos.user.model.email == username
        ).all()
        # breakpoint()
    except DbException:
        raise
    return ViewCartDto(
        items = [ViewCartItemDto(product = BaseProductDto(name=value[0], description=value[1], price=value[2]), quantity=value[3]) for value in values]
        )

    

