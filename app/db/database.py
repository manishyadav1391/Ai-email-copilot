from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # avoids connection timeout issues
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()