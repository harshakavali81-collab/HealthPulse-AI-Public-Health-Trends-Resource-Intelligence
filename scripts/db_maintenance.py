"""SQLite maintenance for local HealthPulse aggregate data: integrity and safe backups.

Run from repository root: python scripts/db_maintenance.py verify
No individual-level records are stored; database remains local and untracked.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile


def database_path() -> Path:
    return Path(os.getenv("HEALTHPULSE_DB", str(Path(__file__).resolve().parents[1] / "data" / "healthpulse.db")))


def inspect_database(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Database does not exist: {path}")
    # Open read-only: running verify must never silently create an empty DB.
    with sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True) as conn:
        status = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if status != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {status}")
        exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='observations'").fetchone()
        if not exists:
            raise ValueError("Not a HealthPulse database: observations table missing")
        rows = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
        counts = dict(conn.execute("SELECT source, COUNT(*) FROM observations GROUP BY source").fetchall())
        return {"integrity": "ok", "observations": rows, "sources": counts, "database": str(path)}


def backup_database(source: Path, destination: Path) -> dict:
    if not source.is_file():
        raise FileNotFoundError(f"Cannot back up missing database: {source}")
    if source.resolve() == destination.resolve():
        raise ValueError("Source and backup paths must be different")
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite an existing backup: {destination}")
    inspect_database(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # SQLite's online backup API copies a transactionally consistent snapshot,
    # even if another process writes to the source database.
    fd, name = tempfile.mkstemp(prefix=".healthpulse-", suffix=".sqlite.tmp", dir=destination.parent)
    os.close(fd)
    temporary = Path(name)
    try:
        with sqlite3.connect(f"file:{source.resolve().as_posix()}?mode=ro", uri=True) as src:
            with sqlite3.connect(temporary) as dest:
                src.backup(dest, pages=100, sleep=0.05)
        result = inspect_database(temporary)
        os.replace(temporary, destination)
        result["database"] = str(destination)
        return result
    finally:
        temporary.unlink(missing_ok=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify or back up a HealthPulse aggregate SQLite database")
    parser.add_argument("command", choices=["verify", "backup"])
    parser.add_argument("--database", type=Path, default=database_path())
    parser.add_argument("--output", type=Path, help="New backup path (backup only)")
    args = parser.parse_args(argv)
    try:
        if args.command == "backup":
            if not args.output:
                parser.error("backup requires --output")
            result = backup_database(args.database, args.output)
        else:
            result = inspect_database(args.database)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, sqlite3.DatabaseError, RuntimeError, ValueError) as exc:
        print(f"HealthPulse maintenance error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
