from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import init_db
from app.data.seed import seed_database
from app.middleware.tenant import tenant_middleware
from app.routers import products, config, admin
import pathlib, sqlite3

def create_app(db: sqlite3.Connection | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        conn = db if db is not None else init_db()
        seed_database(conn)
        app.state.db = conn
        yield

    app = FastAPI(title="Multi-Tenant Storefront API", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.add_middleware(BaseHTTPMiddleware, dispatch=tenant_middleware)
    app.include_router(products.router)
    app.include_router(config.router)
    app.include_router(admin.router)

    @app.get("/health")
    def health(request: Request):
        db_conn = getattr(request.app.state, "db", None)
        if db_conn is None:
            return {"status": "ok", "tenant_count": 0, "total_products": 0}
        tenant_count = db_conn.execute("SELECT COUNT(*) FROM tenants").fetchone()[0]
        total_products = db_conn.execute("SELECT COUNT(*) FROM products WHERE deleted=0").fetchone()[0]
        return {"status": "ok", "tenant_count": tenant_count, "total_products": total_products}

    static_dir = pathlib.Path("/app/frontend/out")
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
    return app

app = create_app()