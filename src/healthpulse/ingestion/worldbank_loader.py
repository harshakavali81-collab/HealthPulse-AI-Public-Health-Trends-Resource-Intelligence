"""World Bank WDI public health series reader (separate source from WHO GHO).

Network calls are administrator initiated, bounded and read-only until the whole
batch passes validation. Never silently substitute WDI observations for WHO GHO.
Official API: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
"""
from __future__ import annotations
from datetime import datetime, timezone
import re
from urllib.parse import urlsplit
import httpx
from healthpulse.ingestion.public_dataset_loader import COUNTRIES
from healthpulse.processing.clean import INDICATORS
from healthpulse.processing.validate import validate_records

BASE = "https://api.worldbank.org"
DEFAULT_COUNTRIES = tuple(country[0] for country in COUNTRIES)
MIN_YEAR, MAX_YEAR = 2012, 2024
WB_CODES = {
    "life_expectancy": "SP.DYN.LE00.IN",
    "immunization": "SH.IMM.IDPT",
    "physicians": "SH.MED.PHYS.ZS",
    "hospital_beds": "SH.MED.BEDS.ZS",
    "under5_mortality": "SH.DYN.MORT",
}


def _safe_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname != "api.worldbank.org"
            or parsed.username or parsed.password or parsed.port not in (None, 443)
            or not parsed.path.startswith("/v2/") or parsed.fragment):
        raise ValueError("Untrusted World Bank URL")
    return url


def _response(client, url, params):
    _safe_url(url)
    response = client.get(url, params=params)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[0], dict) or not isinstance(payload[1], list):
        raise ValueError("World Bank response is not a documented [metadata, rows] payload")
    return payload


def _all_pages(client, url, params, max_pages):
    first = None
    rows = []
    for page in range(1, max_pages + 1):
        meta, body = _response(client, url, {**params, "page": page})
        try:
            declared_page, pages = int(meta["page"]), int(meta["pages"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("World Bank page metadata missing") from exc
        if declared_page != page or pages < page or pages > max_pages:
            raise ValueError("World Bank pagination incomplete or inconsistent")
        if first is not None and pages != first:
            raise ValueError("World Bank page count changed while reading")
        first = pages
        rows.extend(body)
        if page == pages:
            return rows
    raise ValueError("World Bank pagination truncated")


def fetch_worldbank_indicator(indicator, *, countries=DEFAULT_COUNTRIES,
                              start_year=MIN_YEAR, end_year=MAX_YEAR,
                              max_pages=5, client=None):
    """Fetch one complete bounded indicator batch and verify country metadata.

    No writes. The caller inserts returned rows only after full validation.
    This is WDI data, not the WHO GHO API; provider/source tags remain distinct.
    """
    if indicator not in WB_CODES or indicator not in INDICATORS:
        raise ValueError("Unknown World Bank indicator")
    if not (2010 <= start_year <= end_year <= 2026):
        raise ValueError("Unsupported historical year range")
    if not 1 <= max_pages <= 10:
        raise ValueError("max_pages out of range")
    countries = tuple(dict.fromkeys(countries))
    if not 1 <= len(countries) <= 25 or any(not re.fullmatch("[A-Z]{3}", c) for c in countries):
        raise ValueError("Countries must contain 1-25 ISO3 country codes")
    code = WB_CODES[indicator]
    country_path = ";".join(countries)
    meta_url = f"{BASE}/v2/country/{country_path}"
    data_url = f"{meta_url}/indicator/{code}"
    created = client is None
    if created:
        client = httpx.Client(timeout=25.0, follow_redirects=False)
    try:
        country_rows = _all_pages(client, meta_url, {"format": "json", "per_page": 50}, max_pages)
        lookup = {}
        for row in country_rows:
            if not isinstance(row, dict):
                continue
            iso = str(row.get("id") or "").upper()
            region = row.get("region") or {}
            region_name = region.get("value") if isinstance(region, dict) else None
            region_id = region.get("id") if isinstance(region, dict) else None
            if iso in countries and region_name and region_id not in (None, "", "NA"):
                lookup[iso] = (str(row.get("name") or iso), str(region_name))
        if not lookup:
            raise ValueError("No valid country metadata returned; cannot map regional comparisons")
        data_rows = _all_pages(
            client, data_url,
            {"format": "json", "per_page": 1000, "date": f"{start_year}:{end_year}"},
            max_pages,
        )
        raw = []
        for obj in data_rows:
            if not isinstance(obj, dict) or obj.get("value") is None:
                continue
            if obj.get("obs_status") in ("F", "P"):
                continue  # Exclude provider forecasts and provisional flags.
            iso = str(obj.get("countryiso3code") or "").upper()
            if iso not in lookup:
                continue  # Prevent regional aggregate codes being treated as nations.
            source_indicator = obj.get("indicator") or {}
            if not isinstance(source_indicator, dict) or source_indicator.get("id", "").upper() != code:
                raise ValueError("World Bank response indicator disagrees with requested code")
            name, region = lookup[iso]
            raw.append({
                "indicator": indicator, "country": iso, "country_name": name,
                "region": region, "year": obj.get("date"), "value": obj["value"],
                "source": "WorldBank", "source_url": f"{BASE}/v2/country/{iso}/indicator/{code}?format=json",
                "note": "World Bank WDI, CC BY 4.0; may include modeled/revised estimates; not WHO GHO data",
            })
        validated, errors = validate_records(raw)
        if not validated:
            raise ValueError("No valid World Bank observations")
        if errors:
            raise ValueError(f"World Bank batch contains {len(errors)} invalid observations; no partial import")
        unique = {}
        for row in validated:
            key = (row["indicator"], row["country"], row["year"], row["source"])
            if key in unique and abs(row["value"] - unique[key]["value"]) > 1e-9:
                raise ValueError("Conflicting duplicate World Bank country-year observations")
            unique[key] = row
        return {"records": list(unique.values()), "provider": "World Bank WDI",
                "indicator_code": code, "countries_with_data": len({r["country"] for r in unique.values()}),
                "observations": len(unique), "complete": True,
                "date_range": [start_year, end_year],
                "fetched_at_utc": datetime.now(timezone.utc).isoformat()}
    finally:
        if created:
            client.close()
