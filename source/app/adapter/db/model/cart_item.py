import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.app.adapter.db.model.base import Base
from source.app.adapter.db.repository import SQLRepository
from source.app.domain.cart_item_dto import CartItemDto, CreateCartItemDto


class CartItem(Base):
    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cart.cart_id"), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product_id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class SQLCartItemRepository(SQLRepository):
    model = CartItem
    model_dto = CartItemDto
    create_model_dto = CreateCartItemDto
