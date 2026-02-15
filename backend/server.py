"""AFCA runnable backend (no external dependencies).

Endpoints:
- GET  /health
- GET  /api/providers
- GET  /api/appointments
- POST /api/appointments

Also serves static web assets from ../web.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
DATA_FILE = ROOT / "backend" / "data" / "appointments.json"

PROVIDERS = [
    {
        "id": "doc-001",
        "name": "Dr. Aissatou Ndiaye",
        "specialty": "General Practitioner",
        "country": "Senegal",
        "consultation_fee": 15000,
        "currency": "XOF",
        "verified": True,
    },
    {
        "id": "doc-002",
        "name": "Dr. Koffi Kouame",
        "specialty": "Dermatologist",
        "country": "Côte d'Ivoire",
        "consultation_fee": 25000,
        "currency": "XOF",
        "verified": True,
    },
    {
        "id": "doc-003",
        "name": "Dr. Mariama Camara",
        "specialty": "Pediatrician",
        "country": "Guinea",
        "consultation_fee": 180000,
        "currency": "GNF",
        "verified": True,
    },
]


def load_appointments() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_appointments(items: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")


class AFCAHandler(BaseHTTPRequestHandler):
    server_version = "AFCAHTTP/1.0"

    def _send_json(self, payload: dict | list, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        content = path.read_bytes()
        content_type = "text/plain; charset=utf-8"
        if path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        elif path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            self._send_json({"status": "ok", "service": "afca-backend"})
            return

        if parsed.path == "/api/providers":
            query = parse_qs(parsed.query)
            specialty = (query.get("specialty") or [""])[0].lower().strip()
            country = (query.get("country") or [""])[0].lower().strip()

            providers = PROVIDERS
            if specialty:
                providers = [p for p in providers if specialty in p["specialty"].lower()]
            if country:
                providers = [p for p in providers if country in p["country"].lower()]
            self._send_json({"items": providers, "count": len(providers)})
            return

        if parsed.path == "/api/appointments":
            self._send_json({"items": load_appointments()})
            return

        if parsed.path in ("/", "/index.html"):
            self._send_file(WEB_DIR / "index.html")
            return

        static_target = (WEB_DIR / parsed.path.lstrip("/")).resolve()
        if WEB_DIR in static_target.parents or static_target == WEB_DIR:
            self._send_file(static_target)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/appointments":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "invalid JSON"}, status=HTTPStatus.BAD_REQUEST)
            return

        required = ["patient_name", "provider_id", "scheduled_at", "mode"]
        missing = [f for f in required if not payload.get(f)]
        if missing:
            self._send_json(
                {"error": "missing fields", "fields": missing},
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        appointments = load_appointments()
        new_item = {
            "id": f"apt-{len(appointments)+1:04d}",
            "patient_name": payload["patient_name"],
            "provider_id": payload["provider_id"],
            "scheduled_at": payload["scheduled_at"],
            "mode": payload["mode"],
            "reason": payload.get("reason", ""),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        appointments.append(new_item)
        save_appointments(appointments)
        self._send_json(new_item, status=HTTPStatus.CREATED)


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), AFCAHandler)
    print(f"AFCA backend running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
