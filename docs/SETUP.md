# AFCA Complete Project — Setup Guide

This guide captures the three recommended setup paths and the minimum environment required for productive development.

## Quick Start Options

### 1. Docker (Recommended)
```bash
./quickstart.sh
# select Docker option
```
Expected local services:
- Backend API: `http://localhost:8000/docs`
- pgAdmin: `http://localhost:5050`
- Redis Commander: `http://localhost:8081`

### 2. AI-assisted workflow
Use your preferred coding assistant to plan and implement features incrementally from the PRD.

### 3. Local IDE workflow (VS Code / PyCharm)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Run FastAPI with your configured debug profile.

## Required Environment Variables

Create `backend/.env`:

```env
ENV=dev
DEBUG=true
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/afca_dev
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=<min-32-char-secret>
JWT_REFRESH_SECRET=<min-32-char-secret>
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

Optional integrations:
- `WAVE_API_KEY`
- `PAYTECH_API_KEY`
- `TWILIO_ACCOUNT_SID`

## Database Initialization

```bash
cd backend
alembic upgrade head
```

## Test Commands

Backend:
```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

Mobile:
```bash
cd mobile
flutter test
flutter test --coverage
```

## Troubleshooting

### Port conflicts
```bash
lsof -ti:8000
kill -9 $(lsof -ti:8000)
```

### Docker reset
```bash
docker-compose down -v
docker-compose up -d
```

### Rebuild Python virtual environment
```bash
rm -rf backend/.venv
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
