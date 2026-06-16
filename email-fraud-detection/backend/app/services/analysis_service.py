from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate
from app.ml.predictor import analyze_email


class AnalysisService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_analysis(self, user_id: int, payload: AnalysisCreate) -> Analysis:
        analysis_result = analyze_email(payload.email_raw or "", payload.email_subject, payload.email_from, payload.email_to)
        analysis = Analysis(
            user_id=user_id,
            email_subject=analysis_result["email_subject"],
            email_from=analysis_result["email_from"],
            email_to=analysis_result["email_to"],
            fraud_score=analysis_result["fraud_score"],
            labels=analysis_result["labels"],
            details=analysis_result["details"],
        )
        self.session.add(analysis)
        await self.session.commit()
        await self.session.refresh(analysis)
        return analysis

    async def list_user_analyses(self, user_id: int) -> list[Analysis]:
        result = await self.session.execute(select(Analysis).where(Analysis.user_id == user_id).order_by(Analysis.created_at.desc()))
        return result.scalars().all()

    async def get_summary(self, user_id: int) -> dict[str, float | int]:
        total = await self.session.scalar(select(func.count(Analysis.id)).where(Analysis.user_id == user_id))
        average = await self.session.scalar(select(func.avg(Analysis.fraud_score)).where(Analysis.user_id == user_id))
        analyses = await self.session.execute(select(Analysis.labels).where(Analysis.user_id == user_id))
        labels = analyses.scalars().all()
        total_num = int(total or 0)
        phishing_count = sum(1 for label in labels if label.get("phishing"))
        spam_count = sum(1 for label in labels if label.get("spam"))
        spoofing_count = sum(1 for label in labels if label.get("spoofing"))
        bec_count = sum(1 for label in labels if label.get("bec"))
        return {
            "total_analyses": total_num,
            "average_score": float(average or 0.0),
            "phishing_pct": float(phishing_count / total_num * 100) if total_num else 0.0,
            "spam_pct": float(spam_count / total_num * 100) if total_num else 0.0,
            "spoofing_pct": float(spoofing_count / total_num * 100) if total_num else 0.0,
            "bec_pct": float(bec_count / total_num * 100) if total_num else 0.0,
        }
