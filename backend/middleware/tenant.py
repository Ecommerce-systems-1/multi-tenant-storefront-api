import re
import sqlite3
from fastapi import Request, HTTPException
from app.middleware.rate_limit import RateLimiter

TENANT_ID_RE = re.compile(r"^[a-z0-9\-]+$")
_rate_limiter = RateLimiter(limit=60, window_seconds=60)

SKIP_PATHS = {"/health", "/admin/all-products"}

async def tenant_middleware(request: Request, call_next):
    if request.url.path in SKIP_PATHS or request.url.path.startswith("/static"):
        return await call_next(request)
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(400, "X-Tenant-ID header required")
    if not TENANT_ID_RE.match(tenant_id):
        raise HTTPException(400, "Invalid tenant ID format (use lowercase alphanumeric and hyphens)")
    db: sqlite3.Connection = request.app.state.db
    row = db.execute("SELECT * FROM tenants WHERE id = ?", (tenant_id,)).fetchone()
    if not row:
        raise HTTPException(404, f"Tenant '{tenant_id}' not found")
    if not _rate_limiter.check(tenant_id):
        raise HTTPException(429, "Rate limit exceeded", headers={"Retry-After": "60"})
    request.state.tenant = dict(row)
    return await call_next(request)