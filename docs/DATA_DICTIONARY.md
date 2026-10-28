# Data dictionary

Each observation has: `indicator` (canonical identifier), `country` (ISO-3-style code), `country_name`, `region`, `year` (calendar year), `value` (numeric aggregate), `unit` (indicator-defined measurement), `source` (`synthetic` or `WHO`), `source_url` (metadata provenance), `note` (limitations), `ingested_at` (database UTC timestamp).

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
