# AFCA Run & Development Instructions

## 1) Run Backend + Web App

From repository root:

```bash
python backend/server.py
```

Then open:
- Web App: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`
- Providers API: `http://127.0.0.1:8000/api/providers`

## 2) Smoke-test API with curl

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/api/providers
curl -s -X POST http://127.0.0.1:8000/api/appointments \
  -H 'Content-Type: application/json' \
  -d '{"patient_name":"Awa","provider_id":"doc-001","scheduled_at":"2026-02-20T10:00:00Z","mode":"audio","reason":"Headache"}'
```

## 3) Run Mobile App (Flutter)

Prerequisites:
- Flutter SDK installed
- Android emulator or iOS simulator running

Commands:

```bash
cd mobile
flutter pub get
flutter run
```

> If using Android emulator, app already points to `http://10.0.2.2:8000` for backend access.
