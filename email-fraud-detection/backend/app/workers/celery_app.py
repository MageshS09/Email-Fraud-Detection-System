from celery import Celery

from app.core.config import settings

celery = Celery(
    "email_fraud_detection",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery.conf.task_serializer = "json"
celery.conf.result_serializer = "json"
celery.conf.accept_content = ["json"]
celery.conf.task_track_started = True
celery.conf.result_expires = 3600
