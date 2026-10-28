import os
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("HEALTHPULSE_DB", str(tmp_path / "test.db"))
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)
    with TestClient(app) as c:
        yield c
