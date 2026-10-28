<div align="center">

# 🩺 HealthPulse AI

### Public Health Trends & Resource Intelligence

**Full-stack analytics · WHO GHO integration · Forecasting · Explainable visualizations**

![HealthPulse dashboard preview](assets/dashboard-preview.png)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688?style=flat-square&logo=fastapi&logoColor=white) ![React](https://img.shields.io/badge/React-Vite-149ECA?style=flat-square&logo=react&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white) ![Tests](https://img.shields.io/badge/Python-automated_tests-16A34A?style=flat-square)

**⚠️ The Docker app loads a checksum-verified historical World Bank WDI snapshot by default and retains separate synthetic demo data. This is not real-time surveillance or clinical decision support.**

</div>

## Overview

An analytics and visualization application for longitudinal aggregate public health indicators. Includes an audited historical World Bank WDI country-level dataset and a separately labeled reproducible synthetic demo; WHO GHO import remains optional and has not been independently verified live.

![Example trend chart](assets/trend-example.png)

## Features

| Capability | Implementation |
|---|---|
| Intelligence dashboard | 4 KPI cards, interactive charts, country and data-source selectors plus interactive provenance, quality and resource-context views |
| Trend analysis | Annual country/region trends, unit-aware views |
| Regional comparison | Unweighted means with country counts and methodology warnings |
| Machine learning | Ridge time-trend projection with chronological MAE and naive baseline |
| Anomaly detection | Robust MAD year-over-year change flags |
| Exploratory clustering | Scaled KMeans over complete country indicator matrix |
| Data validation | Canonical indicator ranges, ISO-style country codes, source separation |
| Provenance | Interactive provenance and coverage pages, source URLs, quality endpoint, ingestion time, CSV export |
| Deployment | Docker Compose API + Nginx React app, named SQLite volume |
| Testing | API and algorithm tests, frontend build CI |

## Visual atlas · 10 original project figures

The dashboard and data charts below are **synthetic demonstrations**. The seven SVG diagrams illustrate real code structure and workflows; none represent measured public-health outcomes.

| Dashboard | Trend example |
|---|---|
| ![Dashboard preview, synthetic data](assets/dashboard-preview.png) | ![Illustrative synthetic annual trend](assets/trend-example.png) |

![Synthetic coverage example](assets/coverage-example.png)

![System architecture](assets/diagrams/01-system-architecture.svg)
![Data ingestion pipeline](assets/diagrams/02-ingestion-pipeline.svg)
![End-to-end project workflow](assets/diagrams/03-project-workflow.svg)

Additional visuals: [database schema](assets/diagrams/04-observation-schema.svg) · [forecast evaluation](assets/diagrams/05-forecast-evaluation.svg) · [API lifecycle](assets/diagrams/06-api-data-lifecycle.svg) · [repository tree](assets/diagrams/07-project-tree.svg). All ten are indexed in [the visual gallery](docs/VISUAL_GALLERY.md).

## Screenshots and diagrams

![Data coverage example](assets/coverage-example.png)

- [Architecture and data-flow diagrams](docs/ARCHITECTURE.md)
- [Model card and limitations](docs/MODEL_CARD.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Security notes](docs/SECURITY.md)
- [Portfolio case study](docs/PORTFOLIO_CASE_STUDY.md)


## Interactive public showcase (synthetic only)

[Explore the browser demo](https://harshakavali81-collab.github.io/harshavardhan-portfolio/healthpulse-demo.html) — works without a backend, with fabricated values and indicator/country/year filters. **This separate static showcase is not a deployment of FastAPI, does not access WHO, and is not the application’s actual seeded database.** Run Docker Compose for the full platform.

## Real public historical dataset — verified in GitHub

**Published snapshot (28 October 2026): 1,026 World Bank WDI historical aggregate observations across 18 countries and five indicator categories.** This is a source-attributed dataset, not fabricated demo data, direct WHO GHO ingestion, live disease surveillance, or clinical validation.

- **[Explore real WDI data in the live portfolio](https://harshakavali81-collab.github.io/harshavardhan-portfolio/healthpulse-worldbank.html)**
- [Download real country-year dataset (JSON)](data/public/worldbank-wdi-2012-2024.json) · [CSV](data/public/worldbank-wdi-2012-2024.csv)
- [SHA-256 provenance and coverage manifest](data/public/worldbank-manifest.json) · [Snapshot methodology](docs/WDI_SNAPSHOT.md)
- [Read-only live API probe (passed)](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40648073095)
- [Browser and mobile export test (passed)](https://github.com/harshakavali81-collab/harshavardhan-portfolio/actions/runs/40648952963)

**Scope:** Requested years 2012–2024. Actual country and year coverage varies by indicator; do not infer unreported values. Hospital-bed data covers 16 of the 18 selected countries in this version. The public WDI explorer reads a verified JSON copy, while the Docker React/FastAPI application automatically loads that same pinned snapshot from its image and selects it by default.

## World Bank WDI public-data pathway (new)

All five existing health-indicator categories are now mapped to **World Bank WDI** public series, imported with a separate `WorldBank` source label (not directly from WHO GHO). The batch is explicitly admin-only and rejects incomplete metadata/pages or invalid values. It is **not** auto-fetched at startup, and public cloud data import has not been claimed.

```bash
PYTHONPATH=src:. python -m scripts.worldbank_probe --indicator life_expectancy --country IND
# If the probe passes and metadata has been reviewed, set ADMIN_API_KEY privately
curl -X POST http://127.0.0.1:8000/api/admin/sync-worldbank/life_expectancy -H 'X-Admin-Key: PRIVATE_SECRET'
```

See [WDI sourcing, attribution and validation](docs/WORLDBANK_SOURCE.md) and [data dictionary](docs/DATA_DICTIONARY.md). The UI offers the optional source in the selector. The default Docker deployment already loads the pinned historical snapshot automatically; the optional administrator import applies only to unmanaged sources and is blocked for pinned datasets.

## Live WHO connectivity status — 28 October 2026

**WHO imports remain blocked pending upstream accessibility and source validation.** A read-only GitHub Actions probe queried four documented OData paths from a GitHub-hosted runner. All four returned **HTTP 500**, including unfiltered life expectancy and the indicator catalogue. This observation only applies to that runner at the stated time; it is not proof of a global WHO outage.

[Inspect the WHO diagnostic job](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40647026669).

The workflow itself is marked completed/successful because its probe step is informational and allowed to fail. **The probe step's outcome was failure.** Therefore the project must not show a 'WHO verified' or 'Live WHO data' success badge. The React/FastAPI container and synthetic demo remain operational independently of WHO.

## Deploy the full FastAPI + React application

A **single-origin deployment image** is provided as `Dockerfile.deploy` and a Render Blueprint as `render.yaml`. The Blueprint explicitly specifies a **paid Starter instance and persistent disk** to keep SQLite data across deploys. It is **not deployed merely by committing**; Render account connection and your billing authorization are required. See [full deployment and smoke-test guide](docs/DEPLOY_RENDER.md), [WHO source evidence](docs/WHO_SOURCE_EVIDENCE.md), and [independent public-health validation gate](docs/VALIDATION_PLAN.md).

```bash
docker build -f Dockerfile.deploy -t healthpulse-all-in-one .
docker run --rm -p 8000:8000 healthpulse-all-in-one
# Same origin: http://localhost:8000/ (React) and /api/health (FastAPI)
```

The old two-container Docker Compose workflow is retained for local development.

## Quick start with Docker

```bash
cp .env.example .env
# Edit ADMIN_API_KEY in .env only if you want to enable WHO imports.
docker compose up --build
```

Open **http://localhost:8080** for the React dashboard and **http://localhost:8000/docs** for interactive FastAPI documentation.

## Run without Docker

```bash
python -m venv .venv
# Activate your virtual environment
pip install -r requirements.txt
PYTHONPATH=src:. uvicorn backend.app.main:app --reload
# In a second terminal
cd frontend
npm install --no-audit --no-fund
npm run dev
```

Use `http://localhost:5173` for the frontend in development. On Windows PowerShell, run `$env:PYTHONPATH="src;."; uvicorn backend.app.main:app --reload` from the project root.

## WHO import — optional, explicit, admin-only

WHO GHO OData docs: https://www.who.int/data/gho/info/gho-odata-api

```bash
# Put a long random key into your untracked .env, then restart the API.
curl -X POST http://localhost:8000/api/admin/sync-who/life_expectancy \
  -H 'X-Admin-Key: YOUR_PRIVATE_ADMIN_KEY'
# Switch dashboard Data source to 'WHO GHO (if synced)'.
```

The loader pages through bounded WHO OData responses, accepts total-population values only, keeps original provenance and drops records outside indicator validation ranges. Currently configured WHO codes are examples that must be checked against the current indicator catalogue. Networking, source changes, missingness and disaggregation may limit import success. A live feed is **not** preconfigured or claimed. Different countries may have different observation years.

## API examples

```bash
curl 'http://localhost:8000/api/health'
curl 'http://localhost:8000/api/indicators'
curl 'http://localhost:8000/api/records?indicator=immunization&source=synthetic'
curl 'http://localhost:8000/api/regional-comparison?indicator=life_expectancy'
curl 'http://localhost:8000/api/forecast?indicator=life_expectancy&country=IND&horizon=3'
curl 'http://localhost:8000/api/anomalies?indicator=immunization&country=NGA'
curl 'http://localhost:8000/api/clusters'
curl 'http://localhost:8000/api/quality'
curl 'http://localhost:8000/api/resources'
```

## Verified historical World Bank data in the full application

The Docker Compose and single-container deployment images include the already-published **1,026-row World Bank WDI snapshot**, and enable `HEALTHPULSE_AUTOLOAD_WDI=1`. On startup, FastAPI compares the packaged JSON SHA-256 against its provenance manifest, validates all records and seeds the SQLite `WorldBank` source transactionally. Its country/year statistics are available in `GET /api/sources`. The UI selects World Bank WDI automatically when populated, or uses the separately labeled synthetic demonstration if unavailable.

This startup seed requires **no WHO connectivity, API key or data download**. It leaves unrelated/manual World Bank records alone unless previously managed through the built-in snapshot marker. The source remains historical and cannot be treated as a live WHO feed.

Direct `uvicorn` startup does not auto-load unless `HEALTHPULSE_AUTOLOAD_WDI=1` is set. Docker Compose and `Dockerfile.deploy` already configure it. A missing or invalid snapshot in an enabled environment raises an error instead of displaying fabricated values as real.

## Data quality and operations

The dashboard includes interactive **Data provenance**, **Quality monitoring** (country-year gaps) and **Resource context** views. Their corresponding API endpoints are documented in `/docs`.

SQLite integrity and consistent backups:

```bash
python scripts/db_maintenance.py verify
python scripts/db_maintenance.py backup --output backups/healthpulse-YYYYMMDD.sqlite
```

See [backup and recovery guide](docs/OPERATIONS.md).

## Testing

```bash
PYTHONPATH=src:. pytest -q
cd frontend && npm install --no-audit --no-fund && npm run build
```

## Repository map

```text
HealthPulse-AI/
├── README.md, requirements.txt, docker-compose.yml, Dockerfile
├── src/healthpulse/
│   ├── ingestion/         # WHO OData + synthetic demo
│   ├── processing/        # Validation, cleaning, aggregation
│   ├── analytics/         # Descriptive analysis, regional comparisons
│   ├── models/            # Forecast, anomalies, clustering
│   └── monitoring/        # Data quality
├── backend/app/           # FastAPI + SQLite
├── frontend/src/          # React dashboard / views / Recharts
├── notebooks/             # Three reproducible walkthroughs
├── docs/                  # Architecture / data dictionary / governance
├── powerbi/               # CSV import and DAX recipe
├── assets/                # Real demo renders and chart examples
├── tests/                 # API, data, ingestion and model checks
└── .github/workflows/     # Continuous integration
```

## Use responsibly

This prototype deliberately separates WHO and synthetic records and makes no patient-specific predictions. Resource-density charts are **not** verified estimates of resource shortage. Forecasts do not have calibrated uncertainty or epidemiological validation. Regional averages are unweighted and should not be interpreted as published WHO regional estimates. Use authoritative metadata, local statistical expertise and revised data for any real policy question.

## Author

**Kavali Harshavardhan** — AI/ML and Data Analytics portfolio project · [GitHub profile](https://github.com/harshakavali81-collab)

*UI is an original dashboard implementation, drawing only general inspiration from modern healthcare analytics design patterns.*

## Deployment safety regression checks

The single-container server mounts React after its registered API routes so `/api/admin/...` remains protected and accessible for its intended disabled response. The World Bank snapshot is pinned to a SHA-256 manifest, and per-indicator WDI admin refresh returns **409 Conflict** when the pinned dataset is managed; this prevents silent source replacement. Invalid write batches are rejected atomically. Docker CI probes frontend + backend, WDI counts and unauthorized admin endpoints, and checks baseline HTTP response headers. This is deployment **verification**, not confirmation of a paid cloud deployment or clinical/policy validation.
