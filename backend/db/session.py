from typing import Generator

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


print("Database URL is ", settings.DATABASE_URL)
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        print("Yield DB !")
        yield db
    finally:
        print("Close DB !")
        db.close()
