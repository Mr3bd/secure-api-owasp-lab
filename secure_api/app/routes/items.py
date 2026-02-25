from fastapi import APIRouter, Request, Depends

from app.auth.deps import get_current_user_claims
from app.security.validation import SearchRequest, FeedbackRequest
from app.logging.security_logger import log_security_event

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/search")
async def search_items(body: SearchRequest, request: Request, claims=Depends(get_current_user_claims)):
    # Secure behavior: do not leak internal query construction
    # Return controlled response only
    return {
        "message": "Search executed (simulated).",
        "query": body.query,
        "limit": body.limit,
        "user": claims.get("sub"),
    }


@router.post("/feedback")
async def submit_feedback(body: FeedbackRequest, request: Request, claims=Depends(get_current_user_claims)):
    # Log potentially suspicious behavior: repeated feedback could be spam, but rate limiting is handled by NGINX
    log_security_event(
        "app.feedback_submitted",
        ip=request.client.host if request.client else None,
        path=str(request.url.path),
        user_id=str(claims.get("sub")),
        details={"email_domain": body.email.split("@")[-1]},
        severity="INFO",
    )

    return {"status": "received"}