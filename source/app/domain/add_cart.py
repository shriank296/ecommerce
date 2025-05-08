import logging
from source.app.domain.exception import DbException, NotEnoughStock
from source.app.ports.db import Repositories
from sqlalchemy.exc import IntegrityError

def add_to_cart(username,product_id,quantity, repos: Repositories):
        product_repo = repos.product
        user_repo = repos.user
        cart_repo = repos.cart
        try:
            product = repos.db.session.query(product_repo.model).filter(product_repo.model.id == product_id).first()
            if not product.stock > quantity:
                raise NotEnoughStock(product.name, product.stock)
            user_id = repos.db.session.query(user_repo.model.id).filter(user_repo.model.email == username).scalar()
            cart = repos.db.session.query(cart_repo.model).filter(cart_repo.model.user_id == user_id).first()
            if cart:
                cart_obj = cart_repo.model_dto(**cart.__dict__)   
            else:
                cart = cart_repo.create_model_dto(user_id = user_id)
                cart_obj = cart_repo.create(cart)         
            cart_item = repos.cart_item.create_model_dto(product_id=product_id, quantity = quantity, cart_id=cart_obj.cart_id)
            cart_item_obj = repos.cart_item.create(cart_item)
            product.stock -= quantity
            logging.info(f"Reduced stock for product {product_id} to {product.stock}")
        except IntegrityError:
             raise DbException
        return cart_item_obj