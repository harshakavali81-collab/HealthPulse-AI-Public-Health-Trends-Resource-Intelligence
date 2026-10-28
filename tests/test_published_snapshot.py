"""Pinned WDI snapshot bootstrapping regression tests with no network."""
import hashlib
import json
import sqlite3
import pytest
from backend.app.db.store import initialize, connect, query
from healthpulse.ingestion.published_snapshot import verify_snapshot, import_verified_snapshot


def test_snapshot_hash_and_source_manifest():
    batch=verify_snapshot()
    assert batch["rows"]==1026 and batch["countries"]==18
    assert len(batch["sha256"])==64
    assert all(r["source"]=="WorldBank" for r in batch["records"])


def test_startup_autoload_enabled_is_repeatable(monkeypatch,tmp_path):
    monkeypatch.setenv("HEALTHPULSE_DB",str(tmp_path/"healthpulse.sqlite"))
    monkeypatch.setenv("HEALTHPULSE_AUTOLOAD_WDI","1")
    first=initialize()
    assert first["wdi"]["action"]=="imported"
    assert len(query("life_expectancy",source="WorldBank"))==234
    assert len(query(source="WorldBank"))==1026
    assert len(query(source="synthetic"))==1170
    second=initialize()
    assert second["wdi"]["action"]=="unchanged"
    with connect() as db:
        assert db.execute("SELECT COUNT(*) FROM source_snapshots").fetchone()[0]==1


def test_startup_autoload_disabled_preserves_synthetic_only(monkeypatch,tmp_path):
    monkeypatch.setenv("HEALTHPULSE_DB",str(tmp_path/"healthpulse.sqlite"))
    monkeypatch.setenv("HEALTHPULSE_AUTOLOAD_WDI","0")
    result=initialize()
    assert result["wdi"]["action"]=="disabled"
    assert len(query(source="WorldBank"))==0
    assert len(query(source="synthetic"))==1170


def test_altered_snapshot_is_rejected_before_any_sqlite_write(tmp_path,monkeypatch):
    source,manifest=(__import__("healthpulse.ingestion.published_snapshot",fromlist=["snapshot_paths"]).snapshot_paths())
    modified=json.loads(source.read_text(encoding="utf-8"))
    modified["records"][0]["value"]=1.0
    altered=tmp_path/"modified.json"
    altered.write_text(json.dumps(modified),encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        verify_snapshot(altered,manifest)
    monkeypatch.setenv("HEALTHPULSE_DB",str(tmp_path/"tampered.sqlite"))
    with sqlite3.connect(tmp_path/"tampered.sqlite") as db:
        from backend.app.db.store import SCHEMA
        db.executescript(SCHEMA)
        with pytest.raises(ValueError,match="checksum"):
            import_verified_snapshot(db,altered,manifest)
        assert db.execute("SELECT COUNT(*) FROM observations").fetchone()[0]==0


def test_source_status_reports_observation_provenance(client):
    response=client.get("/api/sources")
    assert response.status_code==200
    data=response.json()["sources"]
    assert {r["source"] for r in data}=={"synthetic","WHO","WorldBank"}
    assert next(r for r in data if r["source"]=="synthetic")["observations"]==1170
    assert next(r for r in data if r["source"]=="WHO")["available"] is False
