# WHO source verification dossier

**Verified from WHO public documentation as of 2026-10-28**

- WHO's GHO OData documentation identifies the base endpoint `https://ghoapi.azureedge.net/api` and documents retrieval from `/api/WHOSIS_000001` for life expectancy at birth: https://www.who.int/data/gho/info/gho-odata-api
- WHO DTP3 indicator metadata lists `WHS4_100` and defines the immunization target as one-year-old children who received three doses: https://data.who.int/indicators/i/48D7D19/F8E084C

**Not verified**

- A successful live HTTP response from WHO within the execution environment (network/DNS access unavailable).
- End-to-end official data import into a publicly hosted database.
- Harmonized WHO disaggregations, timestamps, and regional populations across all datasets.
- Under-five mortality source mapping, geographic revision handling and comparison validity.

## Verification path

The optional `.github/workflows/who-live-probe.yml` workflow uses a bounded country-specific query, rejects unexpected host changes, conflicting country-year values, incomplete OData pages and invalid rows. It **does not write** to the database. A green workflow certifies only request/structure compatibility for the selected indicator and country at that moment, not health-science validity.

To run locally:

```bash
PYTHONPATH=src:. python -m scripts.who_probe --indicator life_expectancy --country IND
```

Store probe date, exact indicator code, country list, retrieval limits and reviewer notes for a reproducible evidence trail. WHO site metadata may change.

## Observed upstream/API connectivity incident — 2026-10-28 06:57 UTC

The repository's read-only GitHub Actions probe at [diagnostic run 40647026669](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40647026669) received these response codes from a GitHub-hosted runner:

| WHO route | HTTP status |
|---|---|
| /api/Indicator?$top=1 | **500** |
| /api/WHOSIS_000001?$top=1 | **500** |
| /api/WHOSIS_000001?$top=1&$filter=SpatialDim eq 'IND' | **500** |
| /api/DIMENSION/COUNTRY/DimensionValues?$top=1 | **500** |

The initial bounded importer probe also received HTTP 500. No WHO records were imported or stored. The diagnostic workflow displays a green job because it treats its live probe as **informational**; the actual probe step failed and the step summary records that outcome. Do not interpret the workflow's overall green status as source verification.

**Release decision:** Continue synthetic demo operation; defer genuine WHO import and independent comparisons until the upstream source is reachable, dimensional metadata is reviewed, and a full validated ingest completes. An independent live retry can be initiated using GitHub Actions → WHO live connectivity probe, or from a trusted terminal. This is evidence of errors from one runner at one time, not a claim of a global outage.
