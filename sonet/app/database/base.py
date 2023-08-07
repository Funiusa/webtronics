from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from config import url
from fastapi import Depends


class Base(DeclarativeBase):
    pass


engine = create_engine(url=url, echo=True)

LocalSession = Session(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_database():
    Base.metadata.create_all(engine)


def drop_database():
    Base.metadata.drop_all(engine)
