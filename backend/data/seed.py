import random
import sqlite3
from datetime import datetime, timezone

TENANTS = [
    ("styleseek",  "StyleSeek",  "#6366f1", "Find your style.",     "fashion",  "https://placehold.co/200x60/6366f1/white?text=StyleSeek"),
    ("urbankicks", "UrbanKicks", "#f59e0b", "Step up your game.",   "footwear", "https://placehold.co/200x60/f59e0b/white?text=UrbanKicks"),
    ("luxehome",   "LuxeHome",   "#10b981", "Elevate your space.",  "home",     "https://placehold.co/200x60/10b981/white?text=LuxeHome"),
]

PRODUCTS_BY_TENANT = {
    "styleseek":  {"categories": ["tops","bottoms","accessories"], "brands": ["Verano","NordStyle","CozyMade"]},
    "urbankicks": {"categories": ["shoes","sneakers","boots"],     "brands": ["StreetStep","KickCraft","SoleMate"]},
    "luxehome":   {"categories": ["home","decor","bedding"],       "brands": ["NestCo","PureSpace","DwellCraft"]},
}

def seed_database(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, primary_color TEXT NOT NULL,
            tagline TEXT NOT NULL, logo_url TEXT NOT NULL, category_focus TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL REFERENCES tenants(id),
            name TEXT NOT NULL, description TEXT NOT NULL, category TEXT NOT NULL,
            price REAL NOT NULL, color TEXT NOT NULL, brand TEXT NOT NULL,
            sku TEXT NOT NULL, in_stock INTEGER NOT NULL DEFAULT 1,
            deleted INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_products_tenant ON products(tenant_id);
        CREATE INDEX IF NOT EXISTS idx_products_tenant_deleted ON products(tenant_id, deleted);
    """)
    now = datetime.now(timezone.utc).isoformat()
    for tid, name, color, tagline, cat_focus, logo in TENANTS:
        conn.execute(
            "INSERT OR IGNORE INTO tenants VALUES (?,?,?,?,?,?,?)",
            (tid, name, color, tagline, logo, cat_focus, now)
        )
    rng = random.Random(42)
    colors = ["red","blue","green","black","white","grey","navy","brown"]
    adj = ["Premium","Classic","Modern","Sleek","Cozy","Bold","Durable","Lite"]
    for tid, cfg in PRODUCTS_BY_TENANT.items():
        for i in range(1, 51):
            cat = rng.choice(cfg["categories"])
            brand = rng.choice(cfg["brands"])
            color = rng.choice(colors)
            a = rng.choice(adj)
            pid = f"{tid}_prod_{i:03d}"
            conn.execute(
                "INSERT OR IGNORE INTO products VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (pid, tid, f"{a} {cat.title()} #{i}",
                 f"A {a.lower()} {cat} from {brand}. Perfect for any occasion.",
                 cat, round(rng.uniform(9.99, 299.99), 2), color, brand,
                 f"{tid.upper()[:3]}-{i:04d}", 1, 0, now, now)
            )
    conn.commit()