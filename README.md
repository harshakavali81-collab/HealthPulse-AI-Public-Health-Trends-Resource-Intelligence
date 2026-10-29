# 🩺 HealthPulse AI

An analytics and visualization application for longitudinal aggregate public health indicators. Includes an audited historical World Bank WDI country-level dataset and a separately labeled reproducible synthetic demo; WHO GHO import remains optional and has not been independently verified live.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![HealthPulse dashboard preview](<assets/dashboard-preview.png>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

[Explore the browser demo](https://harshakavali81-collab.github.io/harshavardhan-portfolio/healthpulse-demo.html) — works without a backend, with fabricated values and indicator/country/year filters. **This separate static showcase is not a deployment of FastAPI, does not access WHO, and is not the application’s actual seeded database.** Run Docker Compose for the full platform.

## Key Features

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

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![React](https://img.shields.io/badge/React-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence.git
cd HealthPulse-AI-Public-Health-Trends-Resource-Intelligence
```

```bash
cp .env.example .env
# Edit ADMIN_API_KEY in .env only if you want to enable WHO imports.
docker compose up --build
```

Open **http://localhost:8080** for the React dashboard and **http://localhost:8000/docs** for interactive FastAPI documentation.

## Challenges & Solutions

**Repository organization:** this project uses `src/`, `backend/`, `frontend/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

<div align="center">


### Public Health Trends & Resource Intelligence

**Full-stack analytics · WHO GHO integration · Forecasting · Explainable visualizations**



    

**⚠️ The Docker app loads a checksum-verified historical World Bank WDI snapshot by default and retains separate synthetic demo data. This is not real-time surveillance or clinical decision support.**

</div>

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `powerbi/` | Power BI build assets |
| `assets/` | Visual assets |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

