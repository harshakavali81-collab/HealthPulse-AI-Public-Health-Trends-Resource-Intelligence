"""Read-only readiness checks used by the cloud and Docker health probes."""
from backend.app.db.store import connect, initialize, readiness_status


def test_ready_for_initialized_demo_database(client):
    response=client.get("/api/ready")
    assert response.status_code==200
    assert response.json()["ready"] is True


def test_readiness_never_creates_a_missing_database(monkeypatch,tmp_path):
    db=tmp_path/"missing.sqlite"
    monkeypatch.setenv("HEALTHPULSE_DB",str(db))
    assert readiness_status()=={"ready":False,"reason":"database_missing"}
    assert not db.exists()


def test_manged_wdi_incomplete_database_returns_unready(monkeypatch,tmp_path):
    monkeypatch.setenv("HEALTHPULSE_DB",str(tmp_path/"managed.sqlite"))
    monkeypatch.setenv("HEALTHPULSE_AUTOLOAD_WDI","1")
    initialize()
    assert readiness_status()["public_aggregate_rows"]==1026
    with connect() as db:
        db.execute("DELETE FROM observations WHERE source='WorldBank' AND country='IND' AND year=2022")
    assert readiness_status()["reason"]=="managed_wdi_snapshot_inconsistent"
    initialize()
    assert readiness_status()["ready"] is True


def test_empty_existing_database_returns_unready(monkeypatch,tmp_path):
    import sqlite3
    db=tmp_path/"empty.sqlite"
    with sqlite3.connect(db):
        pass
    monkeypatch.setenv("HEALTHPULSE_DB",str(db))
    result=readiness_status()
    assert result["ready"] is False and result["reason"]=="database_unreadable"
