# arzaq/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Используем SQLite с относительным путем
SQLALCHEMY_DATABASE_URL = "sqlite:///./arzaq.db"

# engine = движок, который позволяет SQLAlchemy общаться с БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Необходимо только для SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = класс, от которого наследуются все модели SQLAlchemy
Base = declarative_base()

# Dependency для получения сессии БД в роутерах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()