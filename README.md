# AFCA (Africa First Care Access)

Healthcare, made accessible.

## What's in this repository

- Product and planning documentation in `docs/`
- Initial backend API scaffold in `backend/` (FastAPI)

## Quick start backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.
