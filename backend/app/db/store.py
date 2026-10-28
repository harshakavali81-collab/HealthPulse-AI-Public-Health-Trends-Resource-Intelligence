"""SQLite storage, idempotent startup seed, explicit source provenance."""
import os
import sqlite3
from pathlib import Path
from healthpulse.ingestion.public_dataset_loader import make_demo_data
from healthpulse.processing.validate import validate_records

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
    if not clean:
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
        insert_records(make_demo_data())

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
