from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from application.core.config import config

async_engine = create_async_engine(config.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession)
