import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Set your DATABASE_URL environment variable for production, e.g.:
# postgresql://username:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# For SQLite, need connect_args; for PostgreSQL, not needed
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 