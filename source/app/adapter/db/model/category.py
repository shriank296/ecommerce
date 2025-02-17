from unicodedata import category
import uuid
from typing import Optional
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from source.app.adapter.db.model.base import Base
from sqlalchemy.dialects.postgresql import UUID

class Category(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    parent_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("category.category_id"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(),onupdate=func.now(), nullable=False)
    products = relationship("Product", back_populates="category", cascade="all,delete", lazy="select")
    child_categories: Mapped[list["Category"]] = relationship("Category", back_populates="parent_category", cascade="all,delete", lazy="select")
    parent_category: Mapped[Optional["Category"]] = relationship("Category", back_populates="child_categories",remote_side="Category.id")
