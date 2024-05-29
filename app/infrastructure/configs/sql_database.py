from os import getenv
from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()
database_url = getenv("DATABASE_URL", "")
print("-----------------")
print("DATABASE_URL")
print(database_url)
db_engine = create_engine(database_url)
