"""Checksum-verified, source-attributed World Bank historical snapshot bootstrap.

Safe to run without network access. The pinned dataset is public country/year
aggregate data, not a WHO GHO feed or patient data.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
from healthpulse.ingestion.worldbank_loader import WB_CODES
from healthpulse.processing.validate import validate_records

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "public"


def snapshot_paths():
    return (
        Path(os.getenv("HEALTHPULSE_WDI_SNAPSHOT", str(DATA / "worldbank-wdi-2012-2024.json"))),
        Path(os.getenv("HEALTHPULSE_WDI_MANIFEST", str(DATA / "worldbank-manifest.json"))),
    )


def verify_snapshot(snapshot=None, manifest=None):
    default_json, default_manifest = snapshot_paths()
    snapshot = Path(snapshot or default_json)
    manifest = Path(manifest or default_manifest)
    content = snapshot.read_bytes()
    metadata = json.loads(manifest.read_text(encoding="utf-8"))
    digest = hashlib.sha256(content).hexdigest()
    if metadata.get("source") != "WorldBank" or metadata.get("snapshot_sha256") != digest:
        raise ValueError("World Bank dataset checksum/provenance mismatch")
    document = json.loads(content)
    if document.get("source") != "WorldBank" or document.get("publisher") != metadata.get("publisher"):
        raise ValueError("World Bank document publisher/source mismatch")
    rows = document.get("records")
    if not isinstance(rows, list) or not 0 < len(rows) <= 200000:
        raise ValueError("World Bank snapshot has no valid bounded rows")
    if len(rows) != metadata.get("rows"):
        raise ValueError("World Bank row count does not match audit manifest")
    clean, errors = validate_records(rows)
    if errors or len(clean) != len(rows):
        raise ValueError("World Bank records contain invalid values")
    if len({r["country"] for r in clean}) != metadata.get("countries"):
        raise ValueError("World Bank distinct-country count does not match manifest")
    per_indicator = Counter()
    unique = set()
    for row in clean:
        if (row["source"] != "WorldBank" or
                not row["source_url"].startswith("https://api.worldbank.org/v2/")):
            raise ValueError("World Bank record provenance not trusted")
        key = (row["indicator"], row["country"], row["year"], row["source"])
        if key in unique:
            raise ValueError("Duplicate World Bank year/country/indicator")
        unique.add(key)
        per_indicator[row["indicator"]] += 1
    manifest_groups = metadata.get("indicators", [])
    manifest_counts = {m["indicator"]: m["rows"] for m in manifest_groups}
    if (len(manifest_groups) != len(WB_CODES) or len(manifest_counts) != len(WB_CODES)
            or set(manifest_counts) != set(WB_CODES)
            or manifest_counts != dict(per_indicator)):
        raise ValueError("World Bank per-indicator row counts are inconsistent")
    return {
        "records": clean, "sha256": digest, "rows": len(clean),
        "countries": metadata["countries"],
        "fetched_at_utc": metadata.get("source_fetched_at_utc"),
    }


def import_verified_snapshot(db, snapshot=None, manifest=None):
    """Update managed historical WDI snapshot atomically inside caller transaction.

    Never overwrite an untracked administrator-imported WDI collection.
    A failed checksum/validation leaves the database untouched.
    """
    batch = verify_snapshot(snapshot, manifest)
    row = db.execute("SELECT sha256 FROM source_snapshots WHERE source='WorldBank'").fetchone()
    if row is not None and row[0] == batch["sha256"]:
        return {"action": "unchanged", "rows": batch["rows"]}
    if row is None:
        original = db.execute("SELECT COUNT(*) FROM observations WHERE source='WorldBank'").fetchone()[0]
        if original:
            return {"action": "existing_unmanaged_source_preserved", "rows": original}
    cols = ("indicator", "country", "country_name", "region", "year",
            "value", "unit", "source", "source_url", "note")
    placeholders = ",".join("?" for _ in cols)
    db.execute("DELETE FROM observations WHERE source='WorldBank'")
    db.executemany(
        f"INSERT INTO observations({','.join(cols)}) VALUES({placeholders})",
        [tuple(r[c] for c in cols) for r in batch["records"]],
    )
    db.execute(
        """INSERT INTO source_snapshots(source,sha256,observations,fetched_at_utc)
           VALUES('WorldBank',?,?,?)
           ON CONFLICT(source) DO UPDATE SET sha256=excluded.sha256,
           observations=excluded.observations, fetched_at_utc=excluded.fetched_at_utc""",
        (batch["sha256"], batch["rows"], batch["fetched_at_utc"]),
    )
    return {"action": "imported", "rows": batch["rows"], "sha256": batch["sha256"]}
