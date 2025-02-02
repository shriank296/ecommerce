import uuid
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from source.app.adapter.db.model.base import Base


class CartItem(Base):
    cart_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cart.cart_id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.product_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")