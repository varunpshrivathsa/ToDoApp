import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default to Postgres inside Docker
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://todo_user:secret@db:5432/todo_db"
)

# Important: add pool_pre_ping=True so containers reconnect after restart
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
