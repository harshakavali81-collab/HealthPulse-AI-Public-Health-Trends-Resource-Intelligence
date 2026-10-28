"""FastAPI read-only analytics plus authorized optional WHO data sync."""
from contextlib import asynccontextmanager
import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from healthpulse.processing.clean import INDICATORS
from healthpulse.analytics.descriptive import summarize
from healthpulse.analytics.regional_comparison import compare_regions
from healthpulse.models.forecast import forecast
from healthpulse.models.detect_anomalies import detect_anomalies
from healthpulse.models.cluster_regions import cluster_countries
from healthpulse.monitoring.quality import quality_report
from healthpulse.ingestion.who_loader import fetch_who_indicator
from backend.app.db.store import initialize, insert_records, query

@asynccontextmanager
async def lifespan(app):
    initialize()
    yield

app = FastAPI(title="HealthPulse AI", version="1.0.0", description="Aggregate population-health exploration. Synthetic data by default; not clinical advice.", lifespan=lifespan)
# CORS is unnecessary for Docker nginx proxy or Vite development proxy.
# Explicitly no allow_origins=['*'] for credentialed writes.
app.add_middleware(CORSMiddleware, allow_origins=[], allow_methods=["GET"], allow_headers=[])

def read(indicator=None, country=None, source="synthetic", start_year=None, end_year=None):
    if source not in ("synthetic", "WHO"):
        raise HTTPException(422, "source must be synthetic or WHO")
    return query(indicator, country, source, start_year, end_year)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "healthpulse-api", "version": "1.0.0"}

@app.get("/api/indicators")
def indicators():
    return [{"id": k, **v} for k, v in INDICATORS.items()]

@app.get("/api/records")
def records(indicator: str | None = None, country: str | None = None, source: str = "synthetic", start_year: int | None = None, end_year: int | None = None, limit: int = Query(2500, ge=1, le=5000)):
    if indicator and indicator not in INDICATORS:
        raise HTTPException(422, "Unknown indicator")
    rows = read(indicator, country.upper() if country else None, source, start_year, end_year)
    return {"records": rows[:limit], "total": len(rows), "limited": len(rows)>limit}

@app.get("/api/summary")
def summary(indicator: str = "life_expectancy", source: str = "synthetic"):
    if indicator not in INDICATORS: raise HTTPException(422, "Unknown indicator")
    rows = read(indicator, source=source)
    meta = INDICATORS[indicator]
    return {"indicator": indicator, "source": source, "unit": meta["unit"], **summarize(pd.DataFrame(rows))}

@app.get("/api/regional-comparison")
def regional_comparison(indicator: str = "life_expectancy", source: str = "synthetic", year: int | None = None):
    if indicator not in INDICATORS: raise HTTPException(422, "Unknown indicator")
    rows = read(indicator, source=source)
    return {"indicator": indicator, "unit": INDICATORS[indicator]["unit"], "source": source,
            "aggregation": "unweighted country mean (not population weighted)",
            "regions": compare_regions(pd.DataFrame(rows), year)}

@app.get("/api/trends")
def trends(indicator: str = "life_expectancy", source: str = "synthetic", country: str | None = None):
    if indicator not in INDICATORS: raise HTTPException(422, "Unknown indicator")
    rows = read(indicator, country.upper() if country else None, source)
    if not rows: return {"unit": INDICATORS[indicator]["unit"], "data": []}
    df = pd.DataFrame(rows)
    grouped = df.groupby("year", as_index=False).value.mean().round(2)
    return {"unit": INDICATORS[indicator]["unit"], "aggregation": "country mean; use country filter for one geography", "data": grouped.to_dict(orient="records")}

@app.get("/api/forecast")
def forecast_route(indicator: str = "life_expectancy", country: str = "IND", source: str = "synthetic", horizon: int = Query(3, ge=1, le=5)):
    if indicator not in INDICATORS: raise HTTPException(422, "Unknown indicator")
    rows = read(indicator, country.upper(), source)
    return {"indicator": indicator, "country": country.upper(), "source": source, "unit": INDICATORS[indicator]["unit"], **forecast(rows, indicator, horizon)}

@app.get("/api/anomalies")
def anomalies(indicator: str = "immunization", country: str = "NGA", source: str = "synthetic"):
    if indicator not in INDICATORS: raise HTTPException(422, "Unknown indicator")
    return {"indicator": indicator, "country": country.upper(), "flags": detect_anomalies(read(indicator,country.upper(), source))}

@app.get("/api/clusters")
def clusters(source: str = "synthetic"):
    rows = read(source=source)
    return {"clusters": cluster_countries(pd.DataFrame(rows)), "note": "Exploratory groups only; countries with incomplete indicator coverage excluded."}

@app.get("/api/quality")
def quality(source: str = "synthetic"):
    rows = read(source=source)
    return {"source": source, **quality_report(rows)}

@app.get("/api/resources")
def resource_gaps(source: str = "synthetic"):
    """Visual context only; density indicator is not an estimate of unmet medical need."""
    rows = read("hospital_beds", source=source)
    df = pd.DataFrame(rows)
    if df.empty: return {"countries": [], "note": "No hospital bed density observations for this source."}
    latest = df.sort_values("year").drop_duplicates("country", keep="last").sort_values("value")
    result = latest[["country", "country_name", "value", "year"]].head(12).to_dict(orient="records")
    return {"countries": result, "unit": "beds per 1,000", "note": "Synthetic resource-density illustration; low density does not prove a shortage. Do not make allocation decisions."}

@app.post("/api/admin/sync-who/{indicator}")
def sync_who(indicator: str, x_admin_key: str | None = Header(default=None)):
    import secrets
    key = os.getenv("ADMIN_API_KEY", "")
    if not key:
        raise HTTPException(503, "WHO sync disabled: ADMIN_API_KEY is not configured")
    if not x_admin_key or not secrets.compare_digest(x_admin_key, key):
        raise HTTPException(403, "Invalid admin key")
    if indicator not in INDICATORS or not INDICATORS[indicator].get("who_code"):
        raise HTTPException(422, "No WHO mapping for this indicator")
    try:
        result = fetch_who_indicator(indicator)
        inserted = insert_records(result["records"])
        return {**inserted, "rejected_from_source": result["rejected_count"], "source": "WHO"}
    except Exception as exc:
        raise HTTPException(502, "WHO GHO API could not be queried; check network and source availability") from exc
