# HealthPulse AI — Public Health Trends & Resource Intelligence

**Role:** End-to-end Python, data analytics, machine learning and full-stack portfolio engineering.

## Problem

Population-level indicators are public, but often difficult to compare responsibly. Analysts need a transparent application that shows data coverage, indicator definitions and limitations instead of claiming that all differences imply health outcomes or shortages.

## Solution

HealthPulse AI features a responsive React dashboard and FastAPI analytics service, an optional WHO GHO OData loader, schema validation, provenance-aware SQLite storage, regional comparisons, trend charts, anomaly flags and time-series demonstration projections. Exportable CSVs and API documentation support reproducibility.

## Highlights

- Descriptive comparisons preserve indicator units and declare unweighted country averages.
- Chronological holdout tests the extrapolation model, including a naive baseline.
- Deterministic synthetic records make the application usable offline without inventing official results.
- Dashboard separates WHO data and synthetic demonstration to protect interpretation.
- Docker Compose, automated Python API tests, frontend CI build and methodology documents are included.

## Skills demonstrated

Python, Pandas, NumPy, SQL/SQLite, scikit-learn, FastAPI, React, Vite, Recharts, Docker, testing and GitHub Actions.

## What this project does not claim

It is not a deployed public health surveillance system. It is not clinically validated. It does not diagnose individuals, provide verified resource-gap estimates or produce policy-ready forecasts. WHO synchronization and live hosting must be explicitly configured and verified.

## Recruiter-ready summary

> Built HealthPulse AI, a full-stack aggregate public-health analytics platform using Python, FastAPI, React, SQL and scikit-learn. Delivered indicator monitoring, regional comparisons, forecasting with chronological backtesting, anomaly detection, data-quality checks and CSV exports. Implemented a reproducible synthetic demo, optional WHO data ingestion, automated tests and Docker deployment files with explicit non-clinical safeguards.
