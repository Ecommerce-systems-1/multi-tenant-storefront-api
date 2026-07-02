def test_styleseek_products_not_in_urbankicks(client, styleseek_headers, urbankicks_headers):
    r_ss = client.get("/products?size=100", headers=styleseek_headers)
    r_uk = client.get("/products?size=100", headers=urbankicks_headers)
    ss_ids = {p["id"] for p in r_ss.json()["products"]}
    uk_ids = {p["id"] for p in r_uk.json()["products"]}
    assert ss_ids.isdisjoint(uk_ids), "Cross-tenant product leakage detected"

def test_cannot_access_other_tenant_product_by_id(client, styleseek_headers, db):
    cur = db.execute("SELECT id FROM products WHERE tenant_id='urbankicks' LIMIT 1")
    uk_product_id = cur.fetchone()["id"]
    r = client.get(f"/products/{uk_product_id}", headers=styleseek_headers)
    assert r.status_code == 404

def test_three_tenants_have_independent_catalogs(client, styleseek_headers,
                                                  urbankicks_headers, luxehome_headers):
    for headers in [styleseek_headers, urbankicks_headers, luxehome_headers]:
        r = client.get("/products?size=100", headers=headers)
        assert r.json()["total"] == 50