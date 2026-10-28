# Data dictionary

Each observation has: `indicator` (canonical identifier), `country` (ISO-3-style code), `country_name`, `region`, `year` (calendar year), `value` (numeric aggregate), `unit` (indicator-defined measurement), `source` (`synthetic`, `WHO`, or `WorldBank`), `source_url` (metadata provenance), `note` (limitations), `ingested_at` (database UTC timestamp).

## Indicators

| Code | Definition | Unit | WHO code | Scope |
|---|---|---|---|---|
| life_expectancy | Life expectancy at birth | Years | WHOSIS_000001 | Demo + WHO adapter |
| immunization | DTP3 coverage | Percent | WHS4_100 | Demo + WHO adapter (verify current definition before sync) |
| physicians | Density of physicians | Per 1,000 | None | Demo only |
| hospital_beds | Density of hospital beds | Per 1,000 | None | Demo only |
| under5_mortality | Under-five mortality rate | Per 1,000 live births | WHOSIS_000003 | Demo + WHO adapter (verify current definition before sync) |

Synthetic records are deterministic fabricated examples with seed 42. They are never actual health statistics. `Unmapped` is shown when the WHO API does not supply sufficient reliable WHO region mapping. Country names for unmapped codes remain the code. Comparisons are unweighted means of available countries, not official regional estimates.

Official indicators should always be checked at: https://www.who.int/data/gho/info/gho-odata-api

## World Bank WDI / Indicators API (optional)

The World Bank provider is **distinct from WHO GHO**, with `source="WorldBank"`. It uses the official `api.worldbank.org/v2` JSON API, with country metadata providing *World Bank* regional classifications rather than WHO regions.

| HealthPulse indicator | World Bank WDI code |
|---|---|
| life_expectancy | SP.DYN.LE00.IN |
| immunization | SH.IMM.IDPT |
| physicians | SH.MED.PHYS.ZS |
| hospital_beds | SH.MED.BEDS.ZS |
| under5_mortality | SH.DYN.MORT |

The default importer covers 18 configured countries for 2012–2024, excludes forecast/provisional rows and null observations, rejects incomplete responses, and preserves publisher credit and source URLs. All five series have distinct data quality, collection methods, and update cycles. This importer does **not** imply WHO GHO API availability or verified suitability for planning.

World Bank API reference: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392. License: World Bank Indicators API / WDI data CC BY 4.0 with attribution to the World Bank and original sources where identified.
