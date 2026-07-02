def test_superadmin_can_see_all_products(client):
    r = client.get("/admin/all-products", headers={"X-Admin-Key": "superadmin-secret"})
    assert r.status_code == 200
    assert r.json()["total"] >= 150

def test_regular_admin_cannot_access_superadmin_route(client, styleseek_headers):
    headers = {**styleseek_headers, "X-Admin-Key": "styleseek-admin"}
    r = client.get("/admin/all-products", headers=headers)
    assert r.status_code == 403

def test_no_admin_key_rejected(client):
    r = client.get("/admin/all-products")
    assert r.status_code == 403