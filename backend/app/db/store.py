"""SQLite storage, idempotent startup seed, explicit source provenance."""
import os
import sqlite3
from pathlib import Path
from healthpulse.ingestion.public_dataset_loader import make_demo_data
from healthpulse.processing.validate import validate_records
from healthpulse.ingestion.published_snapshot import import_verified_snapshot

FIELDS = ("indicator", "country", "country_name", "region", "year", "value", "unit", "source", "source_url", "note")
SCHEMA = """
CREATE TABLE IF NOT EXISTS observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  indicator TEXT NOT NULL, country TEXT NOT NULL, country_name TEXT NOT NULL,
  region TEXT NOT NULL, year INTEGER NOT NULL, value REAL NOT NULL, unit TEXT NOT NULL,
  source TEXT NOT NULL, source_url TEXT NOT NULL, note TEXT NOT NULL,
  ingested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(indicator, country, year, source)
);
CREATE INDEX IF NOT EXISTS idx_indicator_source_year ON observations(indicator, source, year);
CREATE TABLE IF NOT EXISTS source_snapshots (
  source TEXT PRIMARY KEY, sha256 TEXT NOT NULL, observations INTEGER NOT NULL,
  fetched_at_utc TEXT
);
"""

def path():
    return os.getenv("HEALTHPULSE_DB", str(Path(__file__).resolve().parents[3] / "data" / "healthpulse.db"))

def connect():
    db_path = Path(path())
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def insert_records(rows):
    clean, errors = validate_records(rows)
    # Never persist the valid subset of an incomplete/invalid import.
    if errors or not clean:
        return {"accepted": 0, "rejected": len(errors), "errors": errors[:5]}
    cols = ", ".join(FIELDS)
    qs = ", ".join(["?"] * len(FIELDS))
    with connect() as db:
        db.executemany(f"INSERT INTO observations({cols}) VALUES({qs}) ON CONFLICT(indicator,country,year,source) DO UPDATE SET country_name=excluded.country_name, region=excluded.region, value=excluded.value, unit=excluded.unit, source_url=excluded.source_url, note=excluded.note, ingested_at=CURRENT_TIMESTAMP", [[r[f] for f in FIELDS] for r in clean])
    return {"accepted": len(clean), "rejected": len(errors), "errors": errors[:5]}

def initialize():
    with connect() as db:
        db.executescript(SCHEMA)
        count = db.execute("SELECT COUNT(*) FROM observations WHERE source='synthetic'").fetchone()[0]
        if count == 0:
            cols = ", ".join(FIELDS)
            placeholders = ",".join("?" for _ in FIELDS)
            db.executemany(
                f"INSERT INTO observations({cols}) VALUES({placeholders})",
                [tuple(r[field] for field in FIELDS) for r in make_demo_data()],
            )
        if os.getenv("HEALTHPULSE_AUTOLOAD_WDI", "0") == "1":
            wdi = import_verified_snapshot(db)
        else:
            wdi = {"action": "disabled"}
    return {"synthetic_seeded": count == 0, "wdi": wdi}


def source_status():
    sources = []
    with connect() as db:
        details = {
            r["source"]: dict(r)
            for r in db.execute(
                """SELECT source, COUNT(*) AS observations,
                          COUNT(DISTINCT country) AS countries,
                          COUNT(DISTINCT indicator) AS indicators
                   FROM observations GROUP BY source"""
            )
        }
        marker = db.execute(
            "SELECT sha256,fetched_at_utc,observations FROM source_snapshots WHERE source='WorldBank'"
        ).fetchone()
    for source in ("synthetic", "WHO", "WorldBank"):
        details_for_source = details.get(source) or {}
        entry = {
            "source": source,
            "available": bool(details_for_source.get("observations", 0)),
            "observations": details_for_source.get("observations", 0),
            "countries": details_for_source.get("countries", 0),
            "indicators": details_for_source.get("indicators", 0),
            "provider": {"synthetic": "fabricated demonstration", "WHO": "WHO GHO", "WorldBank": "World Bank WDI"}[source],
        }
        if source == "WorldBank" and marker:
            entry["published_snapshot_sha256"] = marker["sha256"]
            entry["fetched_at_utc"] = marker["fetched_at_utc"]
        sources.append(entry)
    return {"sources": sources}


def query(indicator=None, country=None, source="synthetic", start_year=None, end_year=None):
    sql = "SELECT indicator,country,country_name,region,year,value,unit,source,source_url,note,ingested_at FROM observations WHERE source=?"
    args = [source]
    for key, val in (("indicator", indicator), ("country", country)):
        if val:
            sql += f" AND {key}=?"
            args.append(val)
    if start_year is not None:
        sql += " AND year>=?"; args.append(start_year)
    if end_year is not None:
        sql += " AND year<=?"; args.append(end_year)
    sql += " ORDER BY year, country, indicator"
    with connect() as db:
        return [dict(r) for r in db.execute(sql, args)]

def readiness_status():
    """Check database availability without creating a missing database.

    Operational readiness is not an epidemiological validation statement.
    """
    db_path=Path(path()).resolve()
    if not db_path.is_file():
        return {"ready":False,"reason":"database_missing"}
    try:
        with sqlite3.connect(db_path.as_uri()+"?mode=ro",uri=True,timeout=3) as db:
            result=db.execute("PRAGMA quick_check(1)").fetchone()
            if not result or result[0]!="ok":
                return {"ready":False,"reason":"sqlite_integrity"}
            counts=dict(db.execute("SELECT source,COUNT(*) FROM observations GROUP BY source"))
            if counts.get("synthetic",0)<1:
                return {"ready":False,"reason":"demo_seed_missing"}
            if os.getenv("HEALTHPULSE_AUTOLOAD_WDI","0")=="1":
                marker=db.execute("SELECT observations FROM source_snapshots WHERE source='WorldBank'").fetchone()
                if not marker or marker[0]<1 or marker[0]!=counts.get("WorldBank",0):
                    return {"ready":False,"reason":"managed_wdi_snapshot_inconsistent"}
            return {"ready":True,"sources_available":sum(c>0 for c in counts.values()),
                    "public_aggregate_rows":counts.get("WorldBank",0),
                    "note":"Operational SQLite readiness only; not public-health or source validation"}
    except (sqlite3.Error,OSError):
        return {"ready":False,"reason":"database_unreadable"}
