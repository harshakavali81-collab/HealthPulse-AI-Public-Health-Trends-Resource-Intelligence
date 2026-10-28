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
