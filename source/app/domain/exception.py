from uuid import UUID


class NotEnoughStock(Exception):
    def __init__(self, product_id: UUID, available_quantity: int):
        self.product_id = product_id
        self.available_quantity = available_quantity
        super().__init__(f"Not enough stock for product {product_id}. Available: {available_quantity}")


class DbException(Exception):
    pass        

class EmptyCart(Exception):
    pass