---
title: Multi-Tenant Storefront API
emoji: 🏬
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Multi-Tenant Storefront API

Three isolated tenants share one API. X-Tenant-ID scopes every request; admin keys gate writes; superadmin sees all.

The landing page is an interactive API console — click any endpoint to call the live API.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/config` | Tenant branding (X-Tenant-ID header) |
| GET | `/products` | Tenant catalog, paginated |
| POST | `/products` | Create (X-Admin-Key: <tenant>-admin) |
| DELETE | `/products/{id}` | Soft delete |
| GET | `/admin/all-products` | All tenants (X-Admin-Key: superadmin-secret) |

## Stack

Python 3.11 · FastAPI · SQLite · Pydantic v2 · Next.js 14 (static export) · Tailwind CSS · Docker
