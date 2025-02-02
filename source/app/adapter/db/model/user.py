from enum import Enum
from sqlalchemy import String, DateTime, Enum as SQLAlchemyEnum, func
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSON
from .base import Base
import bcrypt

class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(Base):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[Optional[str]] 
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    _password: Mapped[str] = mapped_column("password",String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    address: Mapped[dict]= mapped_column(JSON)
    role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(),onupdate=func.now(), nullable=False)
    orders = relationship("Order", back_populates="user", cascade="all,delete", lazy="select")
    cart = relationship("Cart", back_populates="user", cascade="all,delete", lazy="select")



    @property
    def password(self):
        raise AttributeError("Password is write only!")
    
    @password.setter
    def password(self, raw_password: str):
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self._password = hashed_password.decode('utf-8')

    def verify_password(self, raw_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode("utf-8"), self._password.encode("utf-8"))


        
        


