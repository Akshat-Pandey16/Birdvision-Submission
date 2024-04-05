from sqlalchemy import Column, Float, Integer, String, Boolean, create_engine
from sqlalchemy.orm import Session, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    count = Column(Integer)


def create_database():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
