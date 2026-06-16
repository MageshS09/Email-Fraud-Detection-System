# Backend - Email Fraud Detection

## Setup

1. Copy `.env.example` to `.env`
2. Update `DATABASE_URL`, `REDIS_URL`, and `SECRET_KEY`

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Database Migration

```bash
alembic upgrade head
```

## API Endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /analysis/`
- `POST /analysis/upload`
- `GET /analysis/history`
- `GET /analysis/summary`
- `GET /users/me`
- `GET /users/`
