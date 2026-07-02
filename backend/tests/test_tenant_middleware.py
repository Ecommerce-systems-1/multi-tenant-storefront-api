def test_missing_tenant_header_returns_400(client):
    r = client.get("/products")
    assert r.status_code == 400
    assert "X-Tenant-ID" in r.json()["detail"]

def test_invalid_tenant_id_format_returns_400(client):
    r = client.get("/products", headers={"X-Tenant-ID": "INVALID TENANT!"})
    assert r.status_code == 400

def test_unknown_tenant_returns_404(client):
    r = client.get("/products", headers={"X-Tenant-ID": "nonexistent"})
    assert r.status_code == 404

def test_valid_tenant_returns_200(client, styleseek_headers):
    r = client.get("/products", headers=styleseek_headers)
    assert r.status_code == 200