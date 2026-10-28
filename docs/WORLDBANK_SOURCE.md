# World Bank WDI public-data integration

The HealthPulse **WorldBank** source is a separate, optionally imported collection of public historical World Development Indicators (WDI) via the [World Bank Indicators API v2](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392), **not** a workaround that mislabels data as WHO GHO.

## Indicators and legal attribution

The five mapping codes and units are listed in [the data dictionary](DATA_DICTIONARY.md). World Bank WDI datasets are commonly published under **CC BY 4.0**, with World Bank attribution; original producer details vary per indicator. Check the World Bank's actual indicator metadata and provider terms before reuse.

Provider series can contain estimates/revisions, missing years or changing definitions. Cross-country unweighted averages are not official country-population-weighted regional rates.

## Data import (admin-only)

1. Prepare a local instance; keep `ADMIN_API_KEY` unset for public read-only usage.
2. Audit metadata and network connectivity. For a bounded live test without database changes:

```bash
PYTHONPATH=src:. python -m scripts.worldbank_probe --indicator life_expectancy
```

3. Configure a long random `ADMIN_API_KEY` in the *private server environment* only. Never commit or expose it in React.
4. Perform a deliberate import using the admin endpoint:

```bash
curl -X POST http://127.0.0.1:8000/api/admin/sync-worldbank/life_expectancy -H 'X-Admin-Key: PRIVATE_SECRET'
```

5. Select **World Bank WDI (if synced)** from the source selector. All API endpoints preserve this source label. Start with life expectancy before importing others.

The importer is all-or-nothing for the validated batch: it fails on incorrect country metadata, API page gaps, conflicting duplicates, bad values or source-code mismatches. The script does not enable anonymous uploads, clinical interpretation or automatic publication.

## Why not silently switch away from WHO?

On 2026-10-28, the WHO OData endpoint returned 500 for four checks from a GitHub runner. That does not establish a global WHO outage or prove that World Bank access is available. The independent WDI option can be validated on its own merits with live tests. WHO records remain labeled WHO, and synthetic observations remain labeled synthetic.

## Public health use warning

This project is a research and hiring portfolio application, not a clinical tool, outbreak detector, resource allocation system or validated forecast. External epidemiology, statistical and privacy review is still needed for policy/clinical use.
