# Security and privacy checklist

- No individual-level medical records or protected health information should be uploaded or included.
- `ADMIN_API_KEY` must be a long random server-side secret. Do not commit `.env`.
- Dashboard and API are intended for an educational research demo. The current response middleware sets baseline browser headers; HTTPS, reverse-proxy rate limits, structured monitoring, backup/recovery, independent security assessment, and operational incident-response procedures remain necessary for production use.
- WHO sync is disabled without a configured admin key. The endpoint is only for explicitly requested data refreshes and is not run automatically.
- No external WHO API call occurs during demo startup or test execution.
- Do not trust indicator comparability across years or countries without source documentation and data quality audits.
- Do not reuse synthetic visualizations in external reports without prominent DEMO labeling.

## Database maintenance

See [backup and recovery instructions](OPERATIONS.md). The backup tool uses SQLite online backup, validates source and destination, refuses overwrite and never commits database files. Do not expose ADMIN_API_KEY to public users or a static frontend.

## 2026 deployment hardening

- The single-origin React static-files mount is deliberately registered **after every API route**, so it cannot shadow protected admin endpoints. Docker CI probes both `/api/admin/sync-who/...` and `/api/admin/sync-worldbank/...`, expecting HTTP 503 when the key is absent.
- An authenticated per-indicator World Bank refresh is blocked with HTTP 409 when the database contains the checksum-pinned published snapshot. Refresh that pinned dataset atomically through the separate reviewed snapshot workflow, rather than silently mixing revisions.
- Any validation failure in `insert_records` aborts the entire batch, rather than persisting the valid subset.
- Baseline HTTP headers include `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, and a restrictive `Permissions-Policy`; API responses request `Cache-Control: no-store`.
- Public `ADMIN_API_KEY` remains unset. If deliberate ingestion is enabled later, use separate authentication, network access controls and edge rate limiting; an API-key header alone is not sufficient for production assurance.
