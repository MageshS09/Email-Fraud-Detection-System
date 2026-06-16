from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.routers import auth, analysis, users
from app.api.dependencies import limiter
from app.core.config import settings
from app.utils.logger import logger


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="1.0.0")
    app.add_middleware(SlowAPIMiddleware)
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request, exc):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
        )

    app.include_router(auth.router)
    app.include_router(analysis.router)
    app.include_router(users.router)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting Email Fraud Detection backend")

    return app
