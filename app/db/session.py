from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import config

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

if SQLALCHEMY_DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set..")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    print("Creating database")
    Base.metadata.create_all(bind=engine)
    
def get_session():
    with SessionLocal() as session:
        yield session