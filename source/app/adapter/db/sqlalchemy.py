import contextlib
from typing import Optional, List
import logging
from psycopg2.errors import UniqueViolation
from sqlalchemy import text, create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from source.app.config import DB_SQL_LOGGING
from source.app.ports.db.adapter import DbAdapter
from sqlalchemy.orm import Session, sessionmaker
from source.app.ports.db.adapter import DbAdapterException

from .exception import DbIntegrityError, UniqueConstraintViolation

class SessionNotInitialised(DbAdapterException):
    pass

logger = logging.getLogger(__name__)



class SQLAlchemyAdapter(DbAdapter):
    def __init__(self,database_uri: str, engine_args: Optional[dict]=None, session_args: Optional[dict]= None):
        assert database_uri, "databse uri must not be an empty string"
        self.database_uri = database_uri
        self.engine_args = engine_args or dict(
            pool_pre_ping = True,
            pool_size = 20,
            max_overflow = 0,
            pool_recycle = 10,
            pool_timeout = 5,
            echo = (DB_SQL_LOGGING != ""),
        )
        if DB_SQL_LOGGING:
            self.engine_args["connect_args"] = {"sslmode": "require"}

        self.session_args = session_args or dict(
            autoflush=False, expire_on_commit=False
        )    
        self.engine = self.create_engine()
        self._sessions: List[Session] = []

    @property
    def session(self) -> Session:
        if not self._sessions:
            raise SessionNotInitialised
        return self._sessions[-1] 
    
    def destroy_db(self):
        from .model.base import Base

        logger.info("Dropping databse tables from models")
        Base.metadata.drop_all(bind=self.engine)

        with self.engine.connect() as con:
            con.execute(text("DROP IF TABLE EXISTS alembic_version"))
            con.commit()

    def init_db(self):
        from .model.base import Base
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def create_engine(self):
        logger.debug("Setting up a new database engine")
        engine = create_engine(self.database_uri, **self.engine_args)

        return engine

    def session_maker(self):
        logger.debug("Setting up a new local session")
        engine = self.session_args.get("bind")
        if not engine:
            engine = self.engine
        return sessionmaker(bind=engine, **self.session_args)

    @contextlib.contextmanager
    def transaction(self):
        try:
            Session = self.session_maker()
            with Session() as session:
                self._sessions.append(session)    
            try:
                yield session
                session.commit()
            finally:
                self._sessions.pop()
        except (IntegrityError, UniqueViolation) as err:
            raise UniqueConstraintViolation(str(err))
        except SQLAlchemyError as err:
            raise DbIntegrityError(str(err))
        
    def rollback(self):
        """
        
        Rollback or undo unchanges from transaction.
        """
        self.session.rollback()

            