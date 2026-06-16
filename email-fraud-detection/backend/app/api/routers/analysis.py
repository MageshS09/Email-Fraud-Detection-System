from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, limiter
from app.schemas.analysis import AnalysisCreate, AnalysisRead, AnalysisSummary
from app.services.analysis_service import AnalysisService
from app.db.session import async_session

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/", response_model=AnalysisRead)
@limiter.limit("10/minute")
async def create_analysis(payload: AnalysisCreate, current_user=Depends(get_current_user)):
    async with async_session() as session:
        service = AnalysisService(session)
        return await service.create_analysis(current_user.id, payload)


@router.post("/upload", response_model=AnalysisRead)
@limiter.limit("5/minute")
async def upload_email(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    content = await file.read()
    try:
        raw = content.decode("utf-8", errors="replace")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to decode .eml file") from exc
    payload = AnalysisCreate(email_raw=raw, source="upload")
    async with async_session() as session:
        service = AnalysisService(session)
        return await service.create_analysis(current_user.id, payload)


@router.get("/history", response_model=list[AnalysisRead])
async def history(current_user=Depends(get_current_user)):
    async with async_session() as session:
        service = AnalysisService(session)
        return await service.list_user_analyses(current_user.id)


@router.get("/summary", response_model=AnalysisSummary)
async def summary(current_user=Depends(get_current_user)):
    async with async_session() as session:
        service = AnalysisService(session)
        summary_data = await service.get_summary(current_user.id)
        return AnalysisSummary(**summary_data)
