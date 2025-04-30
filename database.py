from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

db_conf = get_settings()

DATABASE_URL = f"postgresql://{db_conf.db_user}:{db_conf.db_password}@{db_conf.db_host}:{db_conf.db_port}/{db_conf.db_name}"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
