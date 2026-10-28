from pathlib import Path
import os
import pytest
from scripts.deployment_smoke import probe

def test_deployment_smoke_refuses_placeholder():
    with pytest.raises(ValueError):
        probe("https://YOUR-ACTUAL-SERVICE.onrender.com")

def test_deployment_smoke_refuses_insecure_http():
    with pytest.raises(ValueError):
        probe("http://example.com")
