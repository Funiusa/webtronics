from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings, url

engine = create_engine(url=url, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
