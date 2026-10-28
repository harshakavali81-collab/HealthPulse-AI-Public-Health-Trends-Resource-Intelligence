# System architecture

```mermaid
flowchart LR
  GHO[WHO GHO OData API] -->|Authorized refresh| ING[Ingestion + validation]
  DEMO[Synthetic generator] --> ING
  ING --> DB[(SQLite data store)]
  DB --> API[FastAPI read-only analytics]
  API --> DASH[React dashboard]
  API --> MODEL[Trends / clustering / flags]
  MODEL --> API
  API --> EXPORT[CSV export]
```

## Trust boundaries

- A secret admin token is mandatory for the opt-in external WHO refresh. Readers can query only aggregate records. No patient data is ingested.
- The HTTP client calls a hard-coded approved WHO host, limits pages and request timeout, and rejects other next-link hosts.
- SQLite enforces country/year/indicator/source uniqueness; validated fields and source provenance are stored with each observation.
- The demo and WHO datasets are never silently combined. UI selections and export filenames always declare the source.
- The default interface displays a clearly labeled deterministic example; it does not claim live measurements.
- Country-level averaging is explicitly unweighted. WHO regional estimates require different methodology.

## Data flow

```mermaid
sequenceDiagram
  participant User
  participant Dashboard
  participant API
  participant Store
  User->>Dashboard: Select indicator and source
  Dashboard->>API: GET /api/records
  API->>Store: Query validated aggregate observations
  Store-->>API: Values + provenance
  API-->>Dashboard: JSON with source metadata
  Dashboard-->>User: Charts, coverage, contextual warnings
```
