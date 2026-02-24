import sqlmodel
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from app.core.config import config

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

if SQLALCHEMY_DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set..")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {})

def init_db():
    print("Creating database")
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session