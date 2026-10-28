"""Strict schema and range validation; no mixing incompatible measurement units."""
from __future__ import annotations
import math

INDICATORS = {
    "life_expectancy": {"name": "Life expectancy at birth", "unit": "years", "min": 0, "max": 125, "higher_better": True, "who_code": "WHOSIS_000001"},
    "immunization": {"name": "DTP3 immunization coverage", "unit": "%", "min": 0, "max": 100, "higher_better": True, "who_code": "WHS4_100"},
    "physicians": {"name": "Physicians density (demo)", "unit": "per 1,000", "min": 0, "max": 30, "higher_better": True, "who_code": None},
    "hospital_beds": {"name": "Hospital bed density (demo)", "unit": "per 1,000", "min": 0, "max": 30, "higher_better": True, "who_code": None},
    "under5_mortality": {"name": "Under-five mortality rate", "unit": "per 1,000 live births", "min": 0, "max": 500, "higher_better": False, "who_code": "WHOSIS_000003"},
}

def normalize_record(row):
    indicator = str(row.get("indicator", ""))
    if indicator not in INDICATORS:
        raise ValueError(f"Unknown indicator: {indicator}")
    year = int(row["year"])
    if not 1950 <= year <= 2100:
        raise ValueError("Year outside allowed range")
    value = float(row["value"])
    conf = INDICATORS[indicator]
    if not math.isfinite(value) or not (conf["min"] <= value <= conf["max"]):
        raise ValueError(f"Value outside {indicator} range")
    country = str(row.get("country", "")).strip().upper()
    if len(country) != 3 or not country.isalpha():
        raise ValueError("Country must be three letter ISO-style code")
    source = str(row.get("source", "synthetic"))
    if source not in ("synthetic", "WHO"):
        raise ValueError("Unsupported source")
    return {
        "indicator": indicator, "country": country, "country_name": str(row.get("country_name") or country),
        "region": str(row.get("region") or "Unmapped"), "year": year, "value": value,
        "unit": conf["unit"], "source": source,
        "source_url": str(row.get("source_url") or ""),
        "note": str(row.get("note") or "")[:500],
    }
