from fastapi import APIRouter, HTTPException, Request, status

from app.auth.jwt import create_access_token
from app.logging.security_logger import log_security_event
from app.security.validation import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])


# Demo users (for lab purposes)
# In real systems, use a proper user store and password hashing.
DEMO_USERS = {
    "alice": {"password": "alice123", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}


@router.post("/login")
async def login(body: LoginRequest, request: Request):
    user = DEMO_USERS.get(body.username)
    if not user or user["password"] != body.password:
        log_security_event(
            "auth.login_failed",
            ip=request.client.host if request.client else None,
            path=str(request.url.path),
            details={"username": body.username},
            severity="WARNING",
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(sub=body.username, role=user["role"])
    return {"access_token": token, "token_type": "bearer"}