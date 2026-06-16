import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.models.user import User
from app.models.analysis import Analysis
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import AnalysisCreate
from app.schemas.user import UserCreate
from app.services.user_service import UserService

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
async def test_create_analysis_and_summary(session):
    user_service = UserService(session)
    user = await user_service.create_user(UserCreate(email='test2@example.com', password='pass1234', full_name='Tester2'))
    analysis_service = AnalysisService(session)
    payload = AnalysisCreate(email_raw='Subject: Offer inside\n\nThis is a special offer', source='paste')
    analysis = await analysis_service.create_analysis(user.id, payload)
    assert analysis.user_id == user.id
    assert analysis.fraud_score >= 0
    summary = await analysis_service.get_summary(user.id)
    assert summary['total_analyses'] == 1
    assert summary['average_score'] == analysis.fraud_score
