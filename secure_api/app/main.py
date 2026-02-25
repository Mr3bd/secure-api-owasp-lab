from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import APP_NAME
from app.routes.auth import router as auth_router
from app.routes.items import router as items_router
from app.routes.admin import router as admin_router
from app.logging.security_logger import log_security_event

app = FastAPI(title=APP_NAME)

app.include_router(auth_router)
app.include_router(items_router)
app.include_router(admin_router)


@app.get("/health")
async def health():
    return {"status": "ok", "app": APP_NAME}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log suspicious payloads / repeated validation failures
    log_security_event(
        "app.validation_failed",
        ip=request.client.host if request.client else None,
        path=str(request.url.path),
        details={"errors": exc.errors()},
        severity="WARNING",
    )
    # Return safe response (do not leak internal info)
    return JSONResponse(status_code=422, content={"detail": "Invalid request payload"})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Avoid leaking stack traces to the client
    log_security_event(
        "app.unhandled_exception",
        ip=request.client.host if request.client else None,
        path=str(request.url.path),
        details={"error": str(exc)},
        severity="ERROR",
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})