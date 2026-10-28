"""WHO GHO OData reader; explicit ingestion, bounds, provenance and total-population filter."""
import httpx
from healthpulse.processing.clean import INDICATORS
from healthpulse.processing.validate import validate_records

BASE = "https://ghoapi.azureedge.net/api"
KNOWN = {"IND": "India", "BGD": "Bangladesh", "NPL": "Nepal", "USA": "United States", "BRA": "Brazil", "CAN": "Canada", "DEU": "Germany", "FRA": "France", "GBR": "United Kingdom", "JPN": "Japan", "AUS": "Australia", "NGA": "Nigeria", "KEN": "Kenya", "ZAF": "South Africa"}

def fetch_who_indicator(indicator: str, max_pages: int = 4, client=None):
    """Retrieve bounded public aggregate records; no personal data or sex-specific mixes."""
    meta = INDICATORS.get(indicator)
    if not meta or not meta.get("who_code"):
        raise ValueError("Indicator has no configured WHO GHO mapping")
    if not 1 <= max_pages <= 10:
        raise ValueError("max_pages out of range")
    url = f"{BASE}/{meta['who_code']}"
    own = client is None
    if own:
        client = httpx.Client(timeout=20.0, follow_redirects=False)
    raw, errors = [], []
    try:
        for _ in range(max_pages):
            # Only permit GHO endpoint; never trust a nextLink host from a response.
            if not url.startswith(BASE + "/"):
                raise ValueError("Untrusted WHO pagination URL")
            res = client.get(url, params={"$top": "1000"} if "?" not in url else None)
            res.raise_for_status()
            payload = res.json()
            for x in payload.get("value", []):
                if x.get("Dim1") not in (None, "", "BTSX", "TOTAL", "TOT"):
                    continue
                if x.get("Dim2") not in (None, "", "TOTAL", "TOT") or x.get("Dim3") not in (None, "", "TOTAL", "TOT"):
                    continue
                if x.get("NumericValue") is None or not x.get("SpatialDim"):
                    continue
                raw.append({"indicator": indicator, "country": str(x["SpatialDim"]), "country_name": KNOWN.get(str(x["SpatialDim"]), str(x["SpatialDim"])),
                            "region": "Unmapped", "year": x.get("TimeDim"), "value": x["NumericValue"],
                            "source": "WHO", "source_url": f"{BASE}/{meta['who_code']}",
                            "note": "WHO GHO aggregate; geography/sex/definition require verification before comparison"})
            link = payload.get("@odata.nextLink", "")
            if not link:
                break
            url = link
        clean, errors = validate_records(raw)
        return {"records": clean, "rejected": errors[:20], "rejected_count": len(errors), "pages_limit": max_pages}
    finally:
        if own:
            client.close()
