import time
from typing import Dict, Tuple

from fastapi import HTTPException, Request

from app.core.config import get_settings


_window_seconds = 60
_requests: Dict[str, Tuple[int, float]] = {}


def _get_client_ip(request: Request) -> str:
    """Extract client IP address from request.

    Args:
        request: Incoming HTTP request.
    Returns:
        str: Client IP address.
    Side Effects:
        None.
    Raises:
        None.
    """

    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def enforce_rate_limit(request: Request) -> None:
    """Enforce a simple IP-based rate limit per minute.

    Args:
        request: Incoming HTTP request.
    Returns:
        None.
    Side Effects:
        Updates in-memory rate limit counters.
    Raises:
        HTTPException: When rate limit is exceeded.
    """

    settings = get_settings()
    ip = _get_client_ip(request)
    now = time.time()
    count, start = _requests.get(ip, (0, now))

    if now - start >= _window_seconds:
        _requests[ip] = (1, now)
        return

    if count >= settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="요청이 너무 많습니다. 잠시 후 다시 시도해주세요.")

    _requests[ip] = (count + 1, start)
