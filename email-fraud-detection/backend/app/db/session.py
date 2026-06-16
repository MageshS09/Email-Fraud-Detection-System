from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.core.config import settings


def get_engine() -> AsyncEngine:
    return create_async_engine(settings.database_url, echo=False, future=True)


engine = get_engine()
async_session = async_sessionmaker(engine, expire_on_commit=False)
