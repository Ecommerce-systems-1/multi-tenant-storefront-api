def test_config_returns_correct_tenant(client, styleseek_headers):
    r = client.get("/config", headers=styleseek_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "styleseek"
    assert data["name"] == "StyleSeek"
    assert data["primary_color"] == "#6366f1"
    assert data["tagline"] == "Find your style."

def test_config_differs_per_tenant(client, styleseek_headers, urbankicks_headers):
    r1 = client.get("/config", headers=styleseek_headers)
    r2 = client.get("/config", headers=urbankicks_headers)
    assert r1.json()["primary_color"] != r2.json()["primary_color"]
    assert r1.json()["tagline"] != r2.json()["tagline"]