import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.models.user import UserRole
from app.services.user_service import UserService
from app.schemas.user import UserCreate

DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


@pytest.fixture(scope='module')
async def session():
    engine = create_async_engine(DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_and_get_user(session):
    service = UserService(session)
    user_in = UserCreate(email='test@example.com', password='password123', full_name='Tester')
    user = await service.create_user(user_in)
    assert user.email == 'test@example.com'
    assert user.role == UserRole.user
    fetched = await service.get_by_email('test@example.com')
    assert fetched is not None
    assert fetched.id == user.id
