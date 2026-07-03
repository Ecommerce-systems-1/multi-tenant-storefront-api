import re
import sqlite3
from fastapi import Request
from fastapi.responses import JSONResponse
from app.middleware.rate_limit import RateLimiter

TENANT_ID_RE = re.compile(r"^[a-z0-9\-]+$")
_rate_limiter = RateLimiter(limit=60, window_seconds=60)

# Only API routes are tenant-scoped; everything else (the static frontend,
# /_next assets, /health, superadmin routes) must pass through untouched.
TENANT_PATHS = ("/products", "/config")


def _error(status_code: int, detail: str, headers: dict | None = None) -> JSONResponse:
    # HTTPException raised inside BaseHTTPMiddleware is not converted to a
    # response by FastAPI's exception handlers; return the response directly.
    return JSONResponse({"detail": detail}, status_code=status_code, headers=headers)


async def tenant_middleware(request: Request, call_next):
    if not request.url.path.startswith(TENANT_PATHS):
        return await call_next(request)
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        return _error(400, "X-Tenant-ID header required")
    if not TENANT_ID_RE.match(tenant_id):
        return _error(400, "Invalid tenant ID format (use lowercase alphanumeric and hyphens)")
    db: sqlite3.Connection = request.app.state.db
    row = db.execute("SELECT * FROM tenants WHERE id = ?", (tenant_id,)).fetchone()
    if not row:
        return _error(404, f"Tenant '{tenant_id}' not found")
    if not _rate_limiter.check(tenant_id):
        return _error(429, "Rate limit exceeded", headers={"Retry-After": "60"})
    request.state.tenant = dict(row)
    return await call_next(request)
