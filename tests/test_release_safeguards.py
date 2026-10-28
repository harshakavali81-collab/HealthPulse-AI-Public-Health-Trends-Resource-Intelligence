"""Regressions for bundled-source integrity and public API routing/security.

These tests make no external network calls.
"""
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.store import insert_records, query
from healthpulse.ingestion.public_dataset_loader import make_demo_data


def test_incomplete_insert_rejects_whole_batch(client):
    valid=dict(make_demo_data()[0])
    valid.update({"indicator": "life_expectancy", "country": "IND", "year": 2040, "value": 80})
    invalid=dict(valid)
    invalid["country"]="not-an-iso3"
    result=insert_records([valid,invalid])
    assert result["accepted"]==0
    assert result["rejected"]==1
    assert query("life_expectancy", "IND", "synthetic",2040,2040)==[]


def test_pinned_worldbank_rejects_authenticated_partial_refresh(tmp_path,monkeypatch):
    monkeypatch.setenv("HEALTHPULSE_DB",str(tmp_path/"protected.sqlite"))
    monkeypatch.setenv("HEALTHPULSE_AUTOLOAD_WDI","1")
    monkeypatch.setenv("ADMIN_API_KEY","very-long-unit-test-value")
    with TestClient(app) as browser:
        before=browser.get("/api/records",params={"source":"WorldBank","indicator":"life_expectancy","limit":1})
        assert before.json()["total"]==234
        response=browser.post("/api/admin/sync-worldbank/life_expectancy",
                              headers={"X-Admin-Key":"very-long-unit-test-value"})
        assert response.status_code==409
        assert "snapshot" in response.json()["detail"].lower()
        after=browser.get("/api/records",params={"source":"WorldBank","indicator":"life_expectancy","limit":1})
        assert after.json()["total"]==before.json()["total"]
        assert after.json()["records"][0]["value"]==before.json()["records"][0]["value"]


def test_baseline_http_headers(client):
    response=client.get("/api/health")
    assert response.headers["x-content-type-options"]=="nosniff"
    assert response.headers["x-frame-options"]=="DENY"
    assert response.headers["referrer-policy"]=="no-referrer"
    assert "camera=()" in response.headers["permissions-policy"]
    assert response.headers["cache-control"]=="no-store"


def test_admin_wdi_route_still_exists_without_credentials(client):
    """In a combined image the route ordering is also checked by Docker CI."""
    response=client.post("/api/admin/sync-worldbank/life_expectancy")
    assert response.status_code==503
