from fastapi import APIRouter, Depends, Request

from app.auth.deps import require_role
from app.logging.security_logger import log_security_event

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def admin_stats(request: Request, claims=Depends(require_role("admin"))):
    # Admin-only endpoint
    log_security_event(
        "admin.stats_accessed",
        ip=request.client.host if request.client else None,
        path=str(request.url.path),
        user_id=str(claims.get("sub")),
        severity="INFO",
    )

    return {
        "uptime": "unknown",
        "users": 1234,
        "note": "This endpoint requires admin role in the secure API.",
    }