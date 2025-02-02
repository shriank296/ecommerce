import uuid
from enum import Enum
from sqlalchemy import DateTime, String, ForeignKey, Enum as SQLAlchemyEnum, DECIMAL, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from source.app.adapter.db.model.base import Base

class Status(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    status: Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), nullable=False)
    total_amount: Mapped[float] = mapped_column(DECIMAL(10,2))
    shipping_address: Mapped[dict] = mapped_column(JSON)
    placed_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(),onupdate=func.now(), nullable=False)
    user = relationship("Order", back_populates="users")
    order_items = relationship("OrderItem", back_populates="order", cascade="all,delete", lazy="select")
