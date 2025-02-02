import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase

# @as_declarative()
class Base(DeclarativeBase):
    "Base class for all models"
    __name__: str
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    @declared_attr
    def id(cls):
        return Column(f"{cls.__tablename__}_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

