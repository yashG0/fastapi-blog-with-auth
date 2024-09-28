from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


SQLITE_DB_URL = "sqlite:///./blogs.db"

engine = create_engine(url=SQLITE_DB_URL, connect_args={"check_same_thread":False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getDB():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
