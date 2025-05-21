import uuid

from sqlalchemy import DECIMAL, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.app.adapter.db.repository import SQLRepository
from source.app.domain.product_dto import BaseProductDto, ProductDto

from .base import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("category.category_id")
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship(
        "CartItem", back_populates="product", cascade="all,delete", lazy="select"
    )


class SQLProductRepository(SQLRepository):
    model = Product
    model_dto = ProductDto
    cart_view_dto = BaseProductDto
