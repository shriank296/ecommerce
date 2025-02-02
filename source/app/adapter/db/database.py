from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from source.app.config import DB_URL

# DATABASE_URL = "postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase"

engine = create_engine(DB_URL, echo=True)