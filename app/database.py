from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

Base = declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping = True)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) 