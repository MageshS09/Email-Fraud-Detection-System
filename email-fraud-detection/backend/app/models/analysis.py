from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    email_subject = Column(String(length=255), nullable=True)
    email_from = Column(String(length=320), nullable=True)
    email_to = Column(String(length=1024), nullable=True)
    fraud_score = Column(Integer, nullable=False)
    labels = Column(JSON, nullable=False)
    details = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")
