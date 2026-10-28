# Security and privacy checklist

- No individual-level medical records or protected health information should be uploaded or included.
- `ADMIN_API_KEY` must be a long random server-side secret. Do not commit `.env`.
- Dashboard and API are intended for an internal research demo. For public production hosting, add authenticated write access, rate limiting, trusted reverse proxy, HTTPS, abuse controls, structured logs, monitoring and backup policies.
- WHO sync is disabled without a configured admin key. The endpoint is only for explicitly requested data refreshes and is not run automatically.
- No external WHO API call occurs during demo startup or test execution.
- Do not trust indicator comparability across years or countries without source documentation and data quality audits.
- Do not reuse synthetic visualizations in external reports without prominent DEMO labeling.
