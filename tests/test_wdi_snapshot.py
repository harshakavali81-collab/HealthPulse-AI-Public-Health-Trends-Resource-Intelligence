"""Offline-only tests for WDI snapshot output and publication."""
import hashlib
import json
from healthpulse.ingestion.worldbank_loader import WB_CODES
from scripts.build_wdi_snapshot import build_snapshot, serialize_snapshot, publish_snapshot

def fake_fetch(indicator,countries):
    idx=list(WB_CODES).index(indicator)
    record={
      "indicator":indicator,"country":"IND","country_name":"India","region":"South Asia",
      "year":2022,"value":20.0+idx,"unit":"years","source":"WorldBank",
      "source_url":"https://api.worldbank.org/v2/country/IND/indicator/"+WB_CODES[indicator]+"?format=json",
      "note":"World Bank WDI",
    }
    return {"complete":True,"records":[record],"countries_with_data":1,
            "fetched_at_utc":"2026-10-28T00:00:00Z"}


def test_snapshot_schema_provenance_and_checksum(tmp_path):
    snapshot=build_snapshot(fake_fetch)
    assert len(snapshot["indicator_manifest"])==5
    assert len(snapshot["records"])==5
    content,manifest,csv_bytes=serialize_snapshot(snapshot)
    audit=json.loads(manifest)
    assert audit["source"]=="WorldBank" and audit["snapshot_sha256"]==hashlib.sha256(content).hexdigest()
    assert b"WorldBank" in csv_bytes
    publish_snapshot(snapshot,tmp_path)
    assert json.loads((tmp_path/"worldbank-wdi-2012-2024.json").read_text())["records"]


def test_snapshot_fails_closed_on_missing_indicator():
    def bad_fetch(indicator,countries):
        if indicator=="physicians":
            raise ConnectionError("Public provider failed")
        return fake_fetch(indicator,countries)
    import pytest
    with pytest.raises(ConnectionError):
        build_snapshot(bad_fetch)


def test_snapshot_fails_on_wrong_source():
    def bad_fetch(indicator,countries):
        batch=fake_fetch(indicator,countries)
        batch["records"][0]["source"]="WHO"
        return batch
    import pytest
    with pytest.raises(RuntimeError,match="Missing/incorrect"):
        build_snapshot(bad_fetch)
