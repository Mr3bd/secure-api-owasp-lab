from typing import Dict, Optional

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError

from app.auth.jwt import decode_and_validate_token
from app.logging.security_logger import log_security_event


def get_bearer_token(authorization: Optional[str] = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization scheme")

    return parts[1].strip()


def get_current_user_claims(token: str = Depends(get_bearer_token)) -> Dict:
    try:
        claims = decode_and_validate_token(token)
        return claims
    except JWTError:
        # App-level suspicious logging (NGINX also logs 401/403/429 at edge)
        log_security_event(
            "auth.jwt_invalid",
            details={"reason": "JWT validation failed"},
            severity="WARNING",
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def require_role(required_role: str):
    def _checker(claims: Dict = Depends(get_current_user_claims)) -> Dict:
        role = claims.get("role")
        if role != required_role:
            log_security_event(
                "auth.forbidden_role",
                user_id=str(claims.get("sub")),
                details={"required": required_role, "provided": role},
                severity="WARNING",
            )
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return claims

    return _checker