import json
import logging
import time
from typing import Any, Dict, Optional

from app.core.config import LOG_LEVEL


def get_security_logger() -> logging.Logger:
    logger = logging.getLogger("security")
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)

    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False
    return logger


def log_security_event(
    event: str,
    *,
    request_id: Optional[str] = None,
    ip: Optional[str] = None,
    path: Optional[str] = None,
    user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    severity: str = "INFO",
) -> None:
    logger = get_security_logger()
    payload = {
        "ts": int(time.time()),
        "event": event,
        "severity": severity,
        "request_id": request_id,
        "ip": ip,
        "path": path,
        "user_id": user_id,
        "details": details or {},
    }
    msg = json.dumps(payload, ensure_ascii=False)
    if severity.upper() == "WARNING":
        logger.warning(msg)
    elif severity.upper() == "ERROR":
        logger.error(msg)
    else:
        logger.info(msg)