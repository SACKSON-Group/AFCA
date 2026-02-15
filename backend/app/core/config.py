from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "AFCA Backend")
    env: str = os.getenv("ENV", "dev")
    otp_ttl_seconds: int = int(os.getenv("OTP_TTL_SECONDS", "300"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
