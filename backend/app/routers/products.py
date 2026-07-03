import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from app.dependencies.auth import require_tenant_admin

router = APIRouter(tags=["products"])


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str
    category: str
    price: float = Field(..., gt=0)
    color: str
    brand: str
    sku: str


@router.get("/products")
def list_products(request: Request, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    db = request.app.state.db
    tid = request.state.tenant["id"]
    total = db.execute(
        "SELECT COUNT(*) FROM products WHERE tenant_id=? AND deleted=0", (tid,)
    ).fetchone()[0]
    rows = db.execute(
        "SELECT * FROM products WHERE tenant_id=? AND deleted=0 ORDER BY id LIMIT ? OFFSET ?",
        (tid, size, (page - 1) * size),
    ).fetchall()
    return {"tenant_id": tid, "total": total, "page": page, "size": size,
            "products": [dict(r) for r in rows]}


@router.get("/products/{product_id}")
def get_product(product_id: str, request: Request):
    db = request.app.state.db
    tid = request.state.tenant["id"]
    row = db.execute(
        "SELECT * FROM products WHERE id=? AND tenant_id=? AND deleted=0",
        (product_id, tid),
    ).fetchone()
    if not row:
        raise HTTPException(404, "Product not found")
    return dict(row)


@router.post("/products", status_code=201, dependencies=[Depends(require_tenant_admin)])
def create_product(body: ProductCreate, request: Request):
    db = request.app.state.db
    tid = request.state.tenant["id"]
    now = datetime.now(timezone.utc).isoformat()
    pid = f"{tid}_prod_{uuid.uuid4().hex[:8]}"
    db.execute(
        "INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (pid, tid, body.name, body.description, body.category, body.price,
         body.color, body.brand, body.sku, 1, 0, now, now),
    )
    db.commit()
    return dict(db.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone())


@router.delete("/products/{product_id}", dependencies=[Depends(require_tenant_admin)])
def delete_product(product_id: str, request: Request):
    db = request.app.state.db
    tid = request.state.tenant["id"]
    cur = db.execute(
        "UPDATE products SET deleted=1 WHERE id=? AND tenant_id=? AND deleted=0",
        (product_id, tid),
    )
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(404, "Product not found")
    return {"deleted": product_id}
