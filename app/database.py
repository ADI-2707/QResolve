from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL


# ==========================
# Database Engine
# ==========================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={
        "check_same_thread": False
    }
)


# ==========================
# Database Session
# ==========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ==========================
# Base Model
# ==========================

Base = declarative_base()


# ==========================
# Dependency
# ==========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()