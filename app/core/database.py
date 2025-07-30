from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
DATABASE_URL = DATABASE_URL.replace("sslmode", "ssl")

Base = declarative_base()

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo = False,
    future = True, 
    pool_size = 20, 
    max_overflow = 0,
    pool_timeout = 60
)

# Create async factory 
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    """Initialize the dat:while condition:
        passabase."""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

# Dependency for getting DB session 
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session: 
        yield session