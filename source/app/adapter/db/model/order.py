import uuid
from enum import Enum

from sqlalchemy import DECIMAL, JSON, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.app.adapter.db.model.base import Base
from source.app.adapter.db.repository import SQLRepository
from source.app.domain.order import OrderDto


class Status(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False
    )
    status: Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), nullable=False)
    total_amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
    shipping_address: Mapped[dict] = mapped_column(JSON)
    placed_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    user = relationship("User", back_populates="orders")
    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all,delete", lazy="select"
    )


class SQLOrderRepository(SQLRepository):
    model = Order
    model_dto = OrderDto
