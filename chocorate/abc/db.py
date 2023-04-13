from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine


def get_default_engine():
    global ENGINE
    if ENGINE:
        raise Exception()

    engine = create_engine(
        "sqlite:///example.db",
        connect_args={"check_same_thread": False},
    )
    set_engine(engine)
    return engine


def create_all(engine):
    SQLModel.metadata.create_all(engine)  # Create tables


def set_engine(engine):
    global ENGINE
    ENGINE = engine


def get_engine():
    global ENGINE
    return ENGINE


def get_session():
    return Session(ENGINE)


ENGINE: Engine = None
