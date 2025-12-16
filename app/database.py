from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Docker verá la carpeta /data gracias al volumen
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/daily_news.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la DB en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()