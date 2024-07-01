from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hitchhiking_diary_server.core.conf import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
