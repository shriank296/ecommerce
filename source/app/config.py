import os

DB_URL = os.environ.get("DB_URL", "")
DB_SQL_LOGGING = os.environ.get("DB_SQL_LOGGING", "")
SECRET_KEY = os.environ.get("SECRET_KEY")
