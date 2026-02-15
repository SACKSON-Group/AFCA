from fastapi import APIRouter, Depends, HTTPException
import base64
from app.core.config import Settings, get_settings
from app.core.otp_store import OtpStore
from app.schemas.auth import OtpRequestIn, OtpVerifyIn, TokenOut

router = APIRouter(prefix="/v1/auth", tags=["auth"])

OTP_STORE: OtpStore | None = None


def get_otp_store(settings: Settings = Depends(get_settings)) -> OtpStore:
    global OTP_STORE
    if OTP_STORE is None:
        OTP_STORE = OtpStore(ttl_seconds=settings.otp_ttl_seconds)
    return OTP_STORE


def _subject(payload: OtpRequestIn | OtpVerifyIn) -> str:
    return payload.phone or payload.email or ""


@router.post("/otp/request")
def request_otp(
    payload: OtpRequestIn,
    settings: Settings = Depends(get_settings),
    otp_store: OtpStore = Depends(get_otp_store),
) -> dict[str, str]:
    subject = _subject(payload)
    code = otp_store.issue(subject)
    response = {"status": "sent"}
    if settings.env == "dev":
        response["dev_code"] = code
    return response


@router.post("/otp/verify", response_model=TokenOut)
def verify_otp(
    payload: OtpVerifyIn,
    otp_store: OtpStore = Depends(get_otp_store),
) -> TokenOut:
    subject = _subject(payload)
    if not otp_store.verify(subject, payload.code):
        raise HTTPException(status_code=400, detail="invalid or expired code")

    raw = f"{subject}:afca".encode("utf-8")
    token = base64.urlsafe_b64encode(raw).decode("utf-8")
    return TokenOut(access_token=token)
