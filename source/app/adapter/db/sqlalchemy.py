from typing import Optional, List
from source.app.config import DB_SQL_LOGGING
from source.app.ports.db.adapter import DbAdapter
from sqlalchemy.orm import Session



class SQLAlchemyAdapter(DbAdapter):
    def __init__(self,database_uri: str, engine_args: Optional[dict]=None, session_args: Optional[dict]= None):
        assert self.database_uri, "databse uri must not be an empty string"
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