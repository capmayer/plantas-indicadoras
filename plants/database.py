from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sql_app.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # check_same_thread is used only for sqlite.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create the base class for future models.
Base = declarative_base()
