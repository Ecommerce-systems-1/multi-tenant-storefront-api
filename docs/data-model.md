# Data Model — Multi-Tenant Storefront API

```sql
CREATE TABLE IF NOT EXISTS tenants (id TEXT PRIMARY KEY, name TEXT NOT NULL, domain TEXT, settings TEXT, is_active INTEGER DEFAULT 1, created_at TEXT DEFAULT (datetime('now')));
```
