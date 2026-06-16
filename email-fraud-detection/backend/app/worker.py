from app.workers.celery_app import celery
from app.ml.predictor import analyze_email


@celery.task(name="app.worker.analyze_email")
def analyze_email_task(raw: str, subject: str | None, from_address: str | None, to_address: str | None) -> dict:
    return analyze_email(raw, subject, from_address, to_address)
