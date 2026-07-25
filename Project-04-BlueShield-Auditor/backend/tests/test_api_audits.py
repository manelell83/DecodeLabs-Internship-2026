"""Integration tests covering the audit -> history -> report API flow.

All tests use mode="demo" so they run deterministically on any OS without
needing admin rights or a real Windows host.
"""


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_demo_audit_succeeds(client):
    response = client.post("/api/v1/audits", json={"mode": "demo"})
    assert response.status_code == 201
    body = response.json()
    assert 0 <= body["score"] <= 100
    assert body["level"] in {"Excellent", "Good", "Fair", "Poor"}
    assert len(body["findings"]) > 0
    assert all(f["source"] == "simulated" for f in body["findings"])


def test_create_audit_rejects_invalid_mode(client):
    response = client.post("/api/v1/audits", json={"mode": "bogus"})
    assert response.status_code == 422


def test_audit_history_lists_created_audits(client):
    client.post("/api/v1/audits", json={"mode": "demo"})
    client.post("/api/v1/audits", json={"mode": "demo"})

    response = client.get("/api/v1/audits")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2


def test_audit_history_filters_by_level(client):
    created = client.post("/api/v1/audits", json={"mode": "demo"}).json()

    matching = client.get("/api/v1/audits", params={"level": created["level"]})
    assert matching.json()["total"] == 1

    non_matching_level = next(l for l in ["Excellent", "Good", "Fair", "Poor"] if l != created["level"])
    non_matching = client.get("/api/v1/audits", params={"level": non_matching_level})
    assert non_matching.json()["total"] == 0


def test_get_audit_detail_by_id(client):
    created = client.post("/api/v1/audits", json={"mode": "demo"}).json()

    response = client.get(f"/api/v1/audits/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_audit_detail_404_for_missing_audit(client):
    response = client.get("/api/v1/audits/9999")
    assert response.status_code == 404


def test_json_report_generation(client):
    created = client.post("/api/v1/audits", json={"mode": "demo"}).json()

    response = client.get(f"/api/v1/audits/{created['id']}/report", params={"format": "json"})
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_pdf_report_generation(client):
    created = client.post("/api/v1/audits", json={"mode": "demo"}).json()

    response = client.get(f"/api/v1/audits/{created['id']}/report", params={"format": "pdf"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_delete_audit(client):
    created = client.post("/api/v1/audits", json={"mode": "demo"}).json()

    delete_response = client.delete(f"/api/v1/audits/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/audits/{created['id']}")
    assert get_response.status_code == 404


def test_stats_endpoint_reflects_created_audits(client):
    client.post("/api/v1/audits", json={"mode": "demo"})

    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["total_audits"] == 1
    assert body["latest_score"] is not None
