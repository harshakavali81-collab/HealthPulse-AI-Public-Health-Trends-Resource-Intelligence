import sqlite3
import pytest
from scripts.db_maintenance import inspect_database, backup_database
from backend.app.db.store import SCHEMA
from healthpulse.ingestion.public_dataset_loader import make_demo_data


def prepare_db(path):
    with sqlite3.connect(path) as db:
        db.executescript(SCHEMA)
        record = make_demo_data()[0]
        db.execute("INSERT INTO observations(indicator,country,country_name,region,year,value,unit,source,source_url,note) VALUES(?,?,?,?,?,?,?,?,?,?)",
                   tuple(record[k] for k in ("indicator","country","country_name","region","year","value","unit","source","source_url","note")))


def test_integrity_and_online_backup(tmp_path):
    source = tmp_path / "source.sqlite"
    target = tmp_path / "backups" / "copy.sqlite"
    prepare_db(source)
    original = inspect_database(source)
    assert original["integrity"] == "ok" and original["observations"] == 1
    result = backup_database(source, target)
    assert target.exists() and result["observations"] == 1
    with sqlite3.connect(target) as db:
        assert db.execute("SELECT COUNT(*) FROM observations WHERE source='synthetic'").fetchone()[0] == 1


def test_prevent_backup_overwrite(tmp_path):
    source = tmp_path / "source.sqlite"
    target = tmp_path / "copy.sqlite"
    prepare_db(source)
    backup_database(source, target)
    with pytest.raises(FileExistsError):
        backup_database(source, target)


def test_verify_missing_database_never_creates_it(tmp_path):
    path = tmp_path / "nonexistent.sqlite"
    with pytest.raises(FileNotFoundError):
        inspect_database(path)
    assert not path.exists()


def test_reject_unrelated_sqlite_db(tmp_path):
    path = tmp_path / "wrong.sqlite"
    with sqlite3.connect(path):
        pass
    with pytest.raises(ValueError, match="Not a HealthPulse"):
        inspect_database(path)


def test_reject_backup_to_same_path(tmp_path):
    source = tmp_path / "source.sqlite"
    prepare_db(source)
    with pytest.raises(ValueError):
        backup_database(source, source)
