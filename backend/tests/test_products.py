def test_product_list_returns_tenant_products(client, styleseek_headers):
    r = client.get("/products", headers=styleseek_headers)
    data = r.json()
    assert data["tenant_id"] == "styleseek"
    assert data["total"] == 50
    assert all(p["tenant_id"] == "styleseek" for p in data["products"])

def test_pagination_size(client, styleseek_headers):
    r = client.get("/products?page=1&size=10", headers=styleseek_headers)
    assert len(r.json()["products"]) == 10

def test_pagination_page_2(client, styleseek_headers):
    r1 = client.get("/products?page=1&size=10", headers=styleseek_headers)
    r2 = client.get("/products?page=2&size=10", headers=styleseek_headers)
    ids1 = {p["id"] for p in r1.json()["products"]}
    ids2 = {p["id"] for p in r2.json()["products"]}
    assert ids1.isdisjoint(ids2)

def test_create_product_requires_admin_key(client, styleseek_headers):
    r = client.post("/products", headers=styleseek_headers,
                    json={"name":"Test","description":"Desc","category":"tops",
                          "price":29.99,"color":"blue","brand":"B","sku":"TEST-001"})
    assert r.status_code == 403

def test_create_product_with_valid_admin(client, styleseek_admin_headers):
    r = client.post("/products", headers=styleseek_admin_headers,
                    json={"name":"New Top","description":"Nice top","category":"tops",
                          "price":39.99,"color":"red","brand":"TestBrand","sku":"NEW-001"})
    assert r.status_code == 201
    assert r.json()["tenant_id"] == "styleseek"

def test_created_product_not_visible_to_other_tenant(client, styleseek_admin_headers,
                                                      urbankicks_headers):
    r = client.post("/products", headers=styleseek_admin_headers,
                    json={"name":"SS Exclusive","description":"Only styleseek","category":"tops",
                          "price":59.99,"color":"black","brand":"SSBrand","sku":"SS-EX-001"})
    new_id = r.json()["id"]
    r2 = client.get(f"/products/{new_id}", headers=urbankicks_headers)
    assert r2.status_code == 404

def test_wrong_tenant_admin_key_rejected(client):
    headers = {"X-Tenant-ID": "styleseek", "X-Admin-Key": "urbankicks-admin"}
    r = client.post("/products", headers=headers,
                    json={"name":"X","description":"X","category":"tops",
                          "price":1.0,"color":"red","brand":"B","sku":"X-001"})
    assert r.status_code == 403

def test_soft_delete_hides_product(client, styleseek_admin_headers, styleseek_headers, db):
    cur = db.execute("SELECT id FROM products WHERE tenant_id='styleseek' LIMIT 1")
    pid = cur.fetchone()["id"]
    r = client.delete(f"/products/{pid}", headers=styleseek_admin_headers)
    assert r.status_code == 200
    r2 = client.get(f"/products/{pid}", headers=styleseek_headers)
    assert r2.status_code == 404