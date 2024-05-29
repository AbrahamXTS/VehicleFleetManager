from sqlmodel import Session, select
from app.infrastructure.configs.sql_database import db_engine
from app.infrastructure.entities.user_entity import User

def add_default_user():
    with Session(db_engine) as session:
        if session.exec(select(User).where(User.email == "root@mail.com")).first():
            return
        user = User(name="Root", last_name="Root", email="root@mail.com", password="$2b$12$AnFLK5tFAvnNnLSpBGjxYOCVP1uRgzTf2s7k4wmN2bkQYk9W3Wsoq")
        session.add(user)
        session.commit()