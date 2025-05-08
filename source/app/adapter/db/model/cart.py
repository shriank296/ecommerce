import uuid
from sqlalchemy import DateTime, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from source.app.adapter.db.model.base import Base
from source.app.adapter.db.repository import SQLRepository
from source.app.domain.cart_dto import CartDto, CreateCartDto

class Cart(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(),onupdate=func.now(), nullable=False)
    user = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart", cascade="all,delete", lazy="select")


class SQLCartRepository(SQLRepository):
    model = Cart
    model_dto = CartDto    
    create_model_dto = CreateCartDto
