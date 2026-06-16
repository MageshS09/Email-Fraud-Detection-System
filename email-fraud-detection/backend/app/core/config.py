from pathlib import Path
from pydantic import BaseSettings, AnyUrl, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "Email Fraud Detection"
    environment: str = Field("production", env="ENVIRONMENT")

    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = Field("HS256", env="ALGORITHM")

    smtp_from_email: str = Field("no-reply@example.com", env="SMTP_FROM_EMAIL")
    rate_limit: str = Field("10/minute", env="RATE_LIMIT")

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
