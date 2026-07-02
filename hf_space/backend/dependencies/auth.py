    from fastapi import Request, HTTPException, Header
    from typing import Optional

    def require_tenant_admin(request: Request, x_admin_key: Optional[str] = Header(None)):
        tenant_id = getattr(request.state, "tenant", {}).get("id", "")
        expected = f"{tenant_id}-admin"
        if x_admin_key != expected:
            raise HTTPException(403, "Valid tenant admin key required")

    def require_superadmin(x_admin_key: Optional[str] = Header(None)):
        if x_admin_key != "superadmin-secret":
            raise HTTPException(403, "Superadmin key required")