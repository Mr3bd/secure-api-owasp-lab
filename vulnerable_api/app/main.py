from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

from app.core.config import APP_NAME
from app.routes.auth import router as auth_router
from app.routes.items import router as items_router

app = FastAPI(title=APP_NAME)

app.include_router(auth_router)
app.include_router(items_router)


@app.get("/health")
async def health():
    return {"status": "ok", "app": APP_NAME}


@app.get("/admin/stats")
async def admin_stats(request: Request):
    """
    Intentionally insecure:
    - No authentication required
    - Leaks information that should be restricted
    """
    return {
        "uptime": "unknown",
        "users": 1234,
        "secrets_hint": "admin endpoints should not be public",
    }


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Intentionally insecure:
    - Returns stack trace to client
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "trace": traceback.format_exc(),
        },
    )