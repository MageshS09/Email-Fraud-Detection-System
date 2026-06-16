import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=320), unique=True, nullable=False, index=True)
    hashed_password = Column(String(length=255), nullable=False)
    full_name = Column(String(length=128), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
