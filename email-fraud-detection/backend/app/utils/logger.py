from loguru import logger


logger.add(
    "backend/logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=False,
)
