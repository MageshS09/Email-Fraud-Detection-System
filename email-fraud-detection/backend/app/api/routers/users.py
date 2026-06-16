from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, require_role
from app.schemas.user import UserRead
from app.services.user_service import UserService
from app.db.session import async_session
from app.models.user import UserRole

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserRead])
async def list_users(current_user=Depends(require_role(UserRole.admin))):
    async with async_session() as session:
        service = UserService(session)
        result = await session.execute(User.__table__.select())
        users = result.scalars().all()
        return users
