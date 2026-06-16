from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.token import Token
from app.services.user_service import UserService
from app.utils.security import create_access_token, verify_password
from app.db.session import async_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(user_create: UserCreate):
    async with async_session() as session:
        service = UserService(session)
        existing = await service.get_by_email(user_create.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = await service.create_user(user_create)
        return user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    async with async_session() as session:
        service = UserService(session)
        user = await service.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        token, expires_at = create_access_token(str(user.email))
        return Token(access_token=token, token_type="bearer", expires_at=expires_at)
