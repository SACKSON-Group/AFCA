from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_otp_flow() -> None:
    req = client.post("/v1/auth/otp/request", json={"phone": "+221701234567"})
    assert req.status_code == 200
    body = req.json()
    assert body["status"] == "sent"
    assert "dev_code" in body

    verify = client.post(
        "/v1/auth/otp/verify",
        json={"phone": "+221701234567", "code": body["dev_code"]},
    )
    assert verify.status_code == 200
    token = verify.json()
    assert token["token_type"] == "bearer"
    assert token["access_token"]


def test_otp_verify_invalid_code() -> None:
    client.post("/v1/auth/otp/request", json={"phone": "+221701234568"})
    response = client.post(
        "/v1/auth/otp/verify",
        json={"phone": "+221701234568", "code": "000000"},
    )
    assert response.status_code == 400
