from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./siesta_sup.db"

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Base class for models
Base = declarative_base()

# Session factory bound to the engine
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    async with async_session_factory() as session:
        yield session
