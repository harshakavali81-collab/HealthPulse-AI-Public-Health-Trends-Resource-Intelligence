# Project structure, data flow and pipelines

## Key implementation boundaries

1. `src/healthpulse/ingestion/`: deterministic synthetic seed and optional WHO GHO OData ingestion.
2. `src/healthpulse/processing/`: clean, validate and guard indicator units, values, geography and source.
3. `backend/app/db/store.py`: upsert into SQLite on `(indicator, country, year, source)`; preserve source URL and ingestion timestamp.
4. `backend/app/main.py`: read-only REST analytics, forecasting, clustering, anomaly and quality endpoints; guarded WHO refresh.
5. `frontend/src/`: source-aware filter controls, four React views and data exports.
6. `tests/`: deterministic validation, API, model and source-adapter checks; GitHub Actions checks Python and frontend build.

## Upstream ingestion DAG

```mermaid
flowchart LR
  A[Synthetic generator] --> C[Normalizer + validator]
  B[Optional WHO GHO OData] --> C
  C --> D[(SQLite observations)]
  D --> E[FastAPI read-only analytics]
  E --> F[React dashboard]
  E --> G[Forecast + clustering + anomalies]
  G --> E
  E --> H[CSV export]
```

## User query sequence

```mermaid
sequenceDiagram
  actor U as Researcher
  participant UI as React
  participant API as FastAPI
  participant DB as SQLite
  U->>UI: Select indicator and source
  UI->>API: GET /api/records?source=synthetic
  API->>DB: Fetch validated source-tagged aggregates
  DB-->>API: Rows + provenance
  API-->>UI: JSON
  UI-->>U: Charts + caveats
```

## Modeling boundaries

A per-country, per-indicator Ridge regression fits annual values. Chronological held-out MAE is compared with a last-observation naive baseline. The model refits on all available years for 1–5-year illustrative extrapolation, clamped to configured indicator bounds. Cluster and anomaly flags are *exploratory*, not policy recommendations or clinical predictions.

## Diagrams

![01-system-architecture.svg](../assets/diagrams/01-system-architecture.svg)

![02-ingestion-pipeline.svg](../assets/diagrams/02-ingestion-pipeline.svg)

![03-project-workflow.svg](../assets/diagrams/03-project-workflow.svg)

![04-observation-schema.svg](../assets/diagrams/04-observation-schema.svg)

![05-forecast-evaluation.svg](../assets/diagrams/05-forecast-evaluation.svg)

![06-api-data-lifecycle.svg](../assets/diagrams/06-api-data-lifecycle.svg)

![07-project-tree.svg](../assets/diagrams/07-project-tree.svg)

See [data dictionary](DATA_DICTIONARY.md), [model card](MODEL_CARD.md), [security](SECURITY.md), [visual gallery](VISUAL_GALLERY.md), and the root README.
