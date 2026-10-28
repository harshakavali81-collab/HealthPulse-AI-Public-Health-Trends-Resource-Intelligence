import pandas as pd
from healthpulse.ingestion.public_dataset_loader import make_demo_data
from healthpulse.analytics.descriptive import summarize
from healthpulse.analytics.regional_comparison import compare_regions
from healthpulse.models.forecast import forecast
from healthpulse.models.detect_anomalies import detect_anomalies
from healthpulse.models.cluster_regions import cluster_countries
from healthpulse.monitoring.quality import quality_report

ROWS = make_demo_data()

def test_summary():
    x = summarize(pd.DataFrame(ROWS))
    assert x["countries"] == 18 and x["observations"] == len(ROWS)

def test_empty_summary():
    assert summarize(pd.DataFrame([]))["observations"] == 0

def test_regions():
    x = compare_regions(pd.DataFrame([r for r in ROWS if r["indicator"] == "life_expectancy"]))
    assert len(x) == 5 and all(z["year"] == 2024 for z in x)

def test_forecast():
    x = forecast([r for r in ROWS if r["country"] == "IND" and r["indicator"] == "life_expectancy"], "life_expectancy", 3)
    assert x["status"] == "ok" and len(x["forecast"]) == 3
    assert x["holdout_mae"] >= 0 and x["baseline_mae"] >= 0

def test_forecast_insufficient():
    x = forecast([r for r in ROWS if r["country"] == "IND" and r["indicator"] == "life_expectancy"][:2], "life_expectancy")
    assert x["status"] == "insufficient_data"

def test_forecast_invalid_horizon():
    import pytest
    with pytest.raises(ValueError): forecast(ROWS, "life_expectancy", 10)

def test_change_flags():
    data = [r for r in ROWS if r["country"] == "NGA" and r["indicator"] == "immunization"]
    years = [r["year"] for r in detect_anomalies(data)]
    assert 2020 in years or 2021 in years

def test_clusters():
    c = cluster_countries(pd.DataFrame(ROWS))
    assert len(c) == 18
    assert set(r["cluster"] for r in c).issubset({0,1,2})

def test_quality():
    q = quality_report(ROWS)
    assert q["rows"] == len(ROWS) and q["duplicate_keys"] == 0
