# Email Fraud Detection System

A production-ready monorepo for detecting email-based threats with an AI-powered backend, React frontend, ML training module, and containerized infrastructure.

## Repository Structure

- `backend/` - FastAPI backend, async SQLAlchemy, JWT auth, Celery tasks, API routes, tests.
- `frontend/` - Vite + React + TypeScript UI for login, analysis, history, and dashboard.
- `ml/` - Training module for email fraud detection models and sample dataset.
- `infrastructure/` - Nginx config for frontend reverse proxy.
- `.github/workflows/ci.yml` - GitHub Actions CI for backend and frontend validation.
- `docker-compose.yml` - Local development stack for backend, frontend/nginx, PostgreSQL, Redis, and Celery worker.
- `.env.example` - Root environment template for backend and frontend services.

## Prerequisites

- `git`
- `Docker` and `docker-compose`
- `Python 3.12` for local backend development
- `Node.js 20` and `npm` for local frontend development

## Setup

1. Clone the repository:

```bash
git clone https://github.com/MageshS09/Email-Fraud-Detection-System.git
cd Email-Fraud-Detection-System/email-fraud-detection
```

2. Copy the environment file:

```bash
cp .env.example .env
```

3. Update `.env` values as needed:

- `DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `VITE_API_BASE`

## Backend

### Install

```bash
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run locally

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database migrations

```bash
cd backend
alembic upgrade head
```

### Backend tests

```bash
cd backend
pytest --maxfail=1 --disable-warnings -q
```

### Backend key files

- `backend/app/main.py` - FastAPI application entrypoint.
- `backend/app/api/routers/` - API route definitions.
- `backend/app/db/session.py` - Async database session factory.
- `backend/app/models/` - SQLAlchemy models.
- `backend/app/services/` - Business logic and analysis service.
- `backend/app/ml/predictor.py` - Model loader for fraud prediction.

## Frontend

### Install

```bash
cd frontend
npm install
```

### Run locally

```bash
cd frontend
npm run dev -- --host 0.0.0.0 --port 4173
```

### Build

```bash
cd frontend
npm run build
```

### Frontend tests

```bash
cd frontend
npm test -- --run
```

### Frontend key files

- `frontend/src/main.tsx` - React app entrypoint.
- `frontend/src/App.tsx` - Route definitions and layout.
- `frontend/src/hooks/useApi.ts` - API client and auth handling.
- `frontend/src/pages/` - Login, register, analysis, history, and dashboard pages.

## ML Module

### Install

```bash
cd ml
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Train model

```bash
cd ml
python train.py
```

The trained model is saved to `ml/models/email_fraud_model.joblib`.

## Docker / Local Stack

### Build and start all services

```bash
docker compose up --build
```

### Stop services

```bash
docker compose down
```

### Services

- `backend` - FastAPI API server on port `8000`
- `nginx` - Serves bundled frontend on port `4173`
- `db` - PostgreSQL database on port `5432`
- `redis` - Redis cache on port `6379`
- `worker` - Celery worker for async tasks

## Environment Variables

Use `.env.example` as a reference for the following values:

- `DATABASE_URL` - SQLAlchemy database connection string
- `REDIS_URL` - Redis connection URL
- `SECRET_KEY` - JWT signing secret
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration
- `ALGORITHM` - JWT algorithm
- `RATE_LIMIT` - API rate limit
- `SMTP_FROM_EMAIL` - Email sender address
- `VITE_API_BASE` - Frontend API base URL

## GitHub Actions CI

The repository contains a CI workflow in `.github/workflows/ci.yml` that:

- installs backend dependencies
- runs database migrations
- executes backend tests
- installs frontend dependencies
- runs frontend tests
- builds the frontend bundle

## Notes

- The backend and frontend can be developed independently during local development.
- If you run into environment-specific package issues, verify Python version `3.12` and `Node.js 20`.
- Use `docker compose logs -f <service>` to inspect runtime logs during containerized development.
