from __future__ import annotations
from typing import Any, Optional, Type, TypeVar
import logging
from uuid import UUID

from pydantic import BaseModel
from source.app.adapter.db.model.base import Base
from source.app.ports.db.repository import Repository
from .sqlalchemy import SQLAlchemyAdapter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import row
from sqlalchemy.orm import Query

from .exception import DbIntegrityError, RecordNotFound

ModelDtoType = Type[BaseModel]
ModelDTO = TypeVar("ModelDTO", bound=BaseModel)

logger = logging.getLogger(__name__)


class SQLRepository(Repository):
    model: Any = Base
    model_dto: ModelDtoType = BaseModel
    def __init__(self, db: SQLAlchemyAdapter):
        self.db: SQLAlchemyAdapter = db

    def validate_obj(self, obj_in: Any):
        pass    

    def model_to_dto(self, db_object):
        if isinstance(db_object, row.Row):
            return self.model_dto(**db_object._mapping)
        # return self.model_dto(**db_object.__dict__)
        return self.model_dto.model_validate(db_object)
    
    def get_query(self) -> Query:
        return self.db.session.query(self.model)
    
    def get_fields(self, fields:str = "all"):
        if fields == "all":
            return []
        raise NotImplementedError(f"Query fields: {fields} not implemented")

    def create(self, obj_in: Any):
        self.validate_obj(obj_in=obj_in)
        db_obj = self.model(**obj_in.model_dump())
        try:
            self.db.session.add(db_obj)
            self.db.session.flush()
        except IntegrityError as err:
            logging.warning(f"DB Integrity Error creating: {self.__class__.__name__}, er: {err}")
            self.db.rollback()
            raise DbIntegrityError(err.orig)
        self.db.session.refresh(db_obj)
        return self.model_to_dto(db_obj)
    
    def read(self, id, **kwargs):
        query = self.get_query().filter(self.model.id == id)
        fields = self.get_fields()
        if fields:
            query = query.with_entities(*fields)
        entity = query.first()
        if not entity:
            raise RecordNotFound(
                f"Model: {self.model.__name__}, Record: {id}, not found."
            )    
        return self.model_to_dto(entity)
    
    def read_multi(self):
        query = self.get_query()
        result = query.all()
        if not result:
            raise RecordNotFound(
                f"Model: {self.model.__name__}, Record not found."
            )
        output = [self.model_to_dto(entity) for entity in result]
        return output
    
    def update(self, id: UUID, obj_in: Any) -> Any:
        assert isinstance(obj_in, BaseModel)
        assert hasattr(obj_in, f"{(self.model.__name__)}_id".lower())
        
        self.validate_obj(obj_in=obj_in)

        if str(getattr(obj_in,f"{(self.model.__name__)}_id".lower())) != str(id):
            raise RecordNotFound("Unable to fetch record. ID in the path does not match id in the payload")
        
        entity = self.db.session.query(self.model).filter(self.model.id == id).first()
        if not entity:
            raise RecordNotFound(
                f"Model: {self.model.__name__}, Record: {id}, not found."
            )
        
        for key, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)
        try:
            self.db.session.add(entity)
            self.db.session.commit()
        except IntegrityError as err:
            logging.warning(f"DB Integrity Error creating: {self.__class__.__name__}, er: {err}")
            self.db.rollback()
            raise DbIntegrityError(err.orig)
        return self.model_to_dto(entity)    
    
    def delete(self, id: UUID) -> bool:
        obj = self.db.session.get(self.model, id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.flush()
            return True
        return False




        




    