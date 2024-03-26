from os import getenv
from sqlmodel import create_engine

database_url = getenv("DATABASE_URL", "")
db_engine = create_engine(database_url)
