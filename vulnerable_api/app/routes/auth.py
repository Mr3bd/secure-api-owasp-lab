from fastapi import APIRouter, Request
from datetime import datetime, timedelta
import base64
import json
import hmac
import hashlib

from app.core.config import JWT_SECRET, JWT_ALG

router = APIRouter(prefix="/auth", tags=["auth"])


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _sign_hs256(message: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode(), message, hashlib.sha256).digest()
    return _b64url(sig)


def issue_token_insecure(sub: str, role: str) -> str:
    """
    Intentionally insecure JWT:
    - Very long expiration (7 days)
    - No issuer/audience
    - Minimal claims
    """
    header = {"alg": JWT_ALG, "typ": "JWT"}
    payload = {
        "sub": sub,
        "role": role,
        "exp": int((datetime.utcnow() + timedelta(days=7)).timestamp()),
    }

    header_b64 = _b64url(json.dumps(header).encode())
    payload_b64 = _b64url(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()

    signature = _sign_hs256(signing_input, JWT_SECRET)
    return f"{header_b64}.{payload_b64}.{signature}"


@router.post("/login")
async def login(body: dict, request: Request):
    """
    Intentionally insecure login:
    - Accepts any username/password (no verification)
    - Role can be user-controlled from request body
    - No rate limiting at app level
    """
    username = str(body.get("username", "guest"))
    role = str(body.get("role", "user"))  # Insecure: user controls role

    token = issue_token_insecure(sub=username, role=role)

    # Insecure: returns token without any real authentication
    return {"access_token": token, "token_type": "bearer"}