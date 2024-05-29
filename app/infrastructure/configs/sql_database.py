from os import getenv
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
database_url = getenv("DATABASE_URL", "")
db_engine = create_engine(database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)