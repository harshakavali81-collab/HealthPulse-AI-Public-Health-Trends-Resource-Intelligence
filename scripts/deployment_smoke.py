"""Smoke test a *real, already deployed* HealthPulse backend and React frontend.

Never creates cloud infrastructure or modifies the deployment.
"""
import argparse
import json
from urllib.parse import urlparse
import httpx


def probe(base_url: str) -> dict:
    u = urlparse(base_url)
    if u.scheme != "https" or not u.hostname or "YOUR-" in base_url.upper():
        raise ValueError("Provide the actual deployed HTTPS service URL, not a placeholder")
    base = base_url.rstrip("/")
    with httpx.Client(timeout=20, follow_redirects=False) as client:
        html = client.get(base + "/")
        html.raise_for_status()
        if "<html" not in html.text.lower() or "healthpulse" not in html.text.lower():
            raise RuntimeError("Root page is not the HealthPulse React dashboard")
        health = client.get(base + "/api/health")
        health.raise_for_status()
        if health.json().get("status") != "ok":
            raise RuntimeError("Health check returned an unexpected status")
        demo = client.get(base + "/api/records", params={"indicator": "life_expectancy", "source": "synthetic", "limit": 2})
        demo.raise_for_status()
        payload = demo.json()
        if not payload.get("records") or any(r.get("source") != "synthetic" for r in payload["records"]):
            raise RuntimeError("Synthetic records were not correctly source-tagged")
        # Never send credentials or real data; ensure unauthenticated writes are blocked.
        block = client.post(base + "/api/admin/sync-who/life_expectancy")
        if block.status_code not in (403, 503):
            raise RuntimeError("Admin sync unexpectedly accepted an unauthenticated request")
        return {"status": "PASS", "base_url": base, "api": health.json(),
                "sample_source": "synthetic", "admin_protected": True,
                "checked": ["frontend_html", "api_health", "source_separation", "unauthorized_write"]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True)
    a = p.parse_args()
    print(json.dumps(probe(a.base_url), indent=2))


if __name__ == "__main__":
    main()
