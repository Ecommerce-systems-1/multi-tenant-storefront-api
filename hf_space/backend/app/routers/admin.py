from fastapi import APIRouter, Depends, Request
from app.dependencies.auth import require_superadmin

router = APIRouter(tags=["admin"])


@router.get("/admin/all-products", dependencies=[Depends(require_superadmin)])
def all_products(request: Request):
    db = request.app.state.db
    rows = db.execute(
        "SELECT * FROM products WHERE deleted=0 ORDER BY tenant_id, id"
    ).fetchall()
    return {"total": len(rows), "products": [dict(r) for r in rows]}
