from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    email_raw: str | None = None
    email_subject: str | None = None
    email_from: str | None = None
    email_to: str | None = None
    source: str = Field("upload", regex="^(upload|paste)$")


class AnalysisRead(BaseModel):
    id: int
    user_id: int
    email_subject: str | None = None
    email_from: str | None = None
    email_to: str | None = None
    fraud_score: int
    labels: dict[str, bool]
    details: dict[str, Any]
    created_at: datetime

    class Config:
        orm_mode = True


class AnalysisSummary(BaseModel):
    total_analyses: int
    average_score: float
    phishing_pct: float
    spam_pct: float
    spoofing_pct: float
    bec_pct: float
