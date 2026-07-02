const BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export async function getConfig(tenantId: string) {
  const r = await fetch(`${BASE}/config`, { headers: { "X-Tenant-ID": tenantId } });
  return r.json();
}

export async function getProducts(tenantId: string, page = 1, size = 20) {
  const r = await fetch(`${BASE}/products?page=${page}&size=${size}`,
    { headers: { "X-Tenant-ID": tenantId } });
  return r.json();
}

export async function createProduct(tenantId: string, adminKey: string, body: object) {
  const r = await fetch(`${BASE}/products`, {
    method: "POST",
    headers: {
      "X-Tenant-ID": tenantId,
      "X-Admin-Key": adminKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}