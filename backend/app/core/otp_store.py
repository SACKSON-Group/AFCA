from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
import secrets


@dataclass
class OtpEntry:
    code: str
    expires_at: datetime


class OtpStore:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, OtpEntry] = {}

    def issue(self, subject: str) -> str:
        code = f"{secrets.randbelow(1000000):06d}"
        expires_at = datetime.now(UTC) + timedelta(seconds=self.ttl_seconds)
        self._store[subject] = OtpEntry(code=code, expires_at=expires_at)
        return code

    def verify(self, subject: str, code: str) -> bool:
        entry = self._store.get(subject)
        if not entry:
            return False
        if datetime.now(UTC) > entry.expires_at:
            self._store.pop(subject, None)
            return False
        if entry.code != code:
            return False
        self._store.pop(subject, None)
        return True
