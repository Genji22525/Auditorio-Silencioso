from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.common.config import settings


def get_engine():
    return create_engine(settings.database_url, pool_pre_ping=True)


def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
