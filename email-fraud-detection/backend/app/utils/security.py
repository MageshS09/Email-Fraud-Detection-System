from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str) -> tuple[str, datetime]:
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expires_at = datetime.utcnow() + expires_delta
    payload = {
        "sub": subject,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, expires_at


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        subject: str | None = payload.get("sub")
        if subject is None:
            raise JWTError("Missing token subject")
        return subject
    except JWTError as exc:
        raise ValueError("Invalid authentication token") from exc
