from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models.user import User, UserRole
from app.services.user_service import UserService
from app.utils.security import decode_access_token
from app.db.session import async_session

security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    token = credentials.credentials
    email = decode_access_token(token)
    async with async_session() as session:
        service = UserService(session)
        user = await service.get_by_email(email)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user


def require_role(role: UserRole):
    async def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != role and current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return role_dependency
