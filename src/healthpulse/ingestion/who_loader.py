"""WHO GHO OData fetcher with strict host, completeness and provenance checks.

A fetch either returns one validated, complete bounded batch or raises before data
is persisted. It does not silently ingest a truncated OData result.
"""
from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urljoin, urlsplit

import httpx
from healthpulse.processing.clean import INDICATORS
from healthpulse.processing.validate import validate_records

BASE = "https://ghoapi.azureedge.net/api"
KNOWN = {
    "IND": "India", "BGD": "Bangladesh", "NPL": "Nepal", "USA": "United States",
    "BRA": "Brazil", "CAN": "Canada", "DEU": "Germany", "FRA": "France",
    "GBR": "United Kingdom", "JPN": "Japan", "AUS": "Australia",
    "NGA": "Nigeria", "KEN": "Kenya", "ZAF": "South Africa",
}
TOTAL_SEX = {None, "", "BTSX", "SEX_BTSX", "TOTAL", "TOT"}
TOTAL_OTHER = {None, "", "TOTAL", "TOT"}


def _validated_url(url: str, code: str) -> str:
    p = urlsplit(url)
    if (p.scheme != "https" or p.hostname != "ghoapi.azureedge.net"
            or p.port not in (None, 443) or p.username or p.password
            or p.path != f"/api/{code}" or p.fragment):
        raise ValueError("Untrusted WHO pagination URL")
    return url


def fetch_who_indicator(indicator: str, max_pages: int = 10, client=None, country: str | None = None):
    """Fetch validated total-population country-year records.

    Optional country filter supports a small, independent live-API probe. Source
    dimension definitions must still be reviewed by public-health experts.
    """
    meta = INDICATORS.get(indicator)
    if not meta or not meta.get("who_code"):
        raise ValueError("Indicator has no configured WHO GHO mapping")
    if not 1 <= max_pages <= 20:
        raise ValueError("max_pages out of range")
    if country is not None and (len(country) != 3 or not country.isalpha() or not country.isupper()):
        raise ValueError("Country filter must be an uppercase three-letter code")
    code = meta["who_code"]
    base_url = f"{BASE}/{code}"
    url = base_url
    own_client = client is None
    if own_client:
        client = httpx.Client(timeout=20, follow_redirects=False)
    raw, accepted = [], []
    visited = set()
    last_link = None
    pages = 0
    try:
        for page in range(max_pages):
            _validated_url(url, code)
            if url in visited:
                raise ValueError("WHO pagination loop detected")
            visited.add(url)
            params = None
            if page == 0:
                params = {"$top": "1000"}
                if country:
                    params["$filter"] = f"SpatialDim eq '{country}'"
            response = client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or not isinstance(payload.get("value"), list):
                raise ValueError("Unexpected WHO OData response structure")
            pages += 1
            for obj in payload["value"]:
                if not isinstance(obj, dict):
                    continue
                if obj.get("Dim1") not in TOTAL_SEX:
                    continue
                if obj.get("Dim2") not in TOTAL_OTHER or obj.get("Dim3") not in TOTAL_OTHER:
                    continue
                if obj.get("SpatialDimType") not in (None, "", "COUNTRY"):
                    continue
                if obj.get("NumericValue") is None or obj.get("SpatialDim") is None:
                    continue
                code3 = str(obj["SpatialDim"]).strip().upper()
                if country and country != code3:
                    continue
                raw.append({
                    "indicator": indicator, "country": code3,
                    "country_name": KNOWN.get(code3, code3),
                    "region": "Unmapped", "year": obj.get("TimeDim"),
                    "value": obj["NumericValue"], "source": "WHO",
                    "source_url": base_url,
                    "note": ("WHO GHO historical aggregate; check dimensional metadata, "
                             "unit and revision history before comparisons"),
                })
            last_link = payload.get("@odata.nextLink") or payload.get("odata.nextLink")
            if not last_link:
                break
            if not isinstance(last_link, str):
                raise ValueError("WHO pagination link is not a string")
            url = urljoin(url, last_link)
            _validated_url(url, code)
        else:
            if last_link:
                raise ValueError("WHO data not fully retrieved: page limit reached")
        clean, errors = validate_records(raw)
        # A malformed total-population measurement must block import, rather
        # than be silently dropped while still reporting a complete batch.
        if errors:
            raise ValueError(f"WHO returned {len(errors)} invalid aggregate observations")
        unique = {}
        for row in clean:
            key = (row["indicator"], row["country"], row["year"], row["source"])
            if key in unique and abs(unique[key]["value"] - row["value"]) > 1e-8:
                raise ValueError("Conflicting WHO observations for same country/year and indicator")
            unique[key] = row
        if not unique:
            raise ValueError("WHO returned no compatible, validated observations")
        return {
            "records": list(unique.values()),
            "rejected": errors[:20],
            "rejected_count": len(errors),
            "pages_fetched": pages,
            "pages_limit": max_pages,
            "complete": True,
            "indicator_code": code,
            "country_filter": country,
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    finally:
        if own_client:
            client.close()
