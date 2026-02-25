from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt, JWTError

from app.core.config import (
    JWT_SECRET,
    JWT_ALG,
    JWT_ISSUER,
    JWT_AUDIENCE,
    JWT_EXPIRE_MINUTES,
)


def create_access_token(sub: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=JWT_EXPIRE_MINUTES)

    claims: Dict[str, Any] = {
        "sub": sub,
        "role": role,
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALG)


def decode_and_validate_token(token: str) -> Dict[str, Any]:
    """
    Validates signature, expiration, issuer, and audience.
    Raises JWTError on failure.
    """
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALG],
        issuer=JWT_ISSUER,
        audience=JWT_AUDIENCE,
        options={"verify_aud": True, "verify_iss": True},
    )