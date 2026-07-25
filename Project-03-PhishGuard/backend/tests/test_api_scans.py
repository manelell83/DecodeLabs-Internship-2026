"""Integration tests covering the scan -> history -> report API flow."""

PHISHING_EMAIL = """From: security@micros0ft-support.com
Subject: Urgent: Verify your account now

Dear user, your Microsoft account will be suspended within 24 hours.
Act now and confirm your password at http://192.168.10.5/verify to avoid suspension.
"""

BENIGN_EMAIL = """From: colleague@example.com
Subject: Lunch tomorrow?

Hey, are we still on for lunch tomorrow at noon?
"""


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_scan_flags_phishing_email(client):
    response = client.post("/api/v1/scans", json={"raw_content": PHISHING_EMAIL})
    assert response.status_code == 201
    body = response.json()
    assert body["risk_score"] > 0
    assert body["risk_level"] in {"Medium", "High", "Critical"}
    assert len(body["indicators"]) > 0
    assert len(body["recommendations"]) > 0


def test_create_scan_on_benign_email_is_low_risk(client):
    response = client.post("/api/v1/scans", json={"raw_content": BENIGN_EMAIL})
    assert response.status_code == 201
    body = response.json()
    assert body["risk_level"] == "Low"
    assert body["indicators"] == []


def test_create_scan_rejects_blank_content(client):
    response = client.post("/api/v1/scans", json={"raw_content": "   "})
    assert response.status_code == 422


def test_scan_history_lists_created_scans(client):
    client.post("/api/v1/scans", json={"raw_content": PHISHING_EMAIL})
    client.post("/api/v1/scans", json={"raw_content": BENIGN_EMAIL})

    response = client.get("/api/v1/scans")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2


def test_get_scan_detail_by_id(client):
    created = client.post("/api/v1/scans", json={"raw_content": PHISHING_EMAIL}).json()

    response = client.get(f"/api/v1/scans/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_scan_detail_404_for_missing_scan(client):
    response = client.get("/api/v1/scans/9999")
    assert response.status_code == 404


def test_json_report_generation(client):
    created = client.post("/api/v1/scans", json={"raw_content": PHISHING_EMAIL}).json()

    response = client.get(f"/api/v1/scans/{created['id']}/report", params={"format": "json"})
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_pdf_report_generation(client):
    created = client.post("/api/v1/scans", json={"raw_content": PHISHING_EMAIL}).json()

    response = client.get(f"/api/v1/scans/{created['id']}/report", params={"format": "pdf"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_delete_scan(client):
    created = client.post("/api/v1/scans", json={"raw_content": BENIGN_EMAIL}).json()

    delete_response = client.delete(f"/api/v1/scans/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/scans/{created['id']}")
    assert get_response.status_code == 404


def test_stats_endpoint_reflects_created_scans(client):
    client.post("/api/v1/scans", json={"raw_content": PHISHING_EMAIL})

    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["total_scans"] == 1
    assert body["average_score"] > 0
