# Deploy the full HealthPulse AI application

**Deployment status:** GitHub source prepared; a real production endpoint must not be claimed until Render creates the service and an HTTPS smoke test succeeds. This deployment configuration is a single Docker container running FastAPI and serving the built React dashboard from the same HTTPS origin.

## Hosting requirements

- You must sign in to a [Render account](https://dashboard.render.com/) and connect GitHub to authorize service creation.
- This repo contains a `render.yaml` Blueprint specifying **Starter compute and a persistent disk**, both of which may incur charges. Review the final costs **before creating a service**. Do not select this setup without accepting the price.
- The blueprint uses a single instance with durable SQLite in `/app/data`. SQLite cannot scale to multiple independent instances. A persistent disk prevents zero-downtime deploys.
- `ADMIN_API_KEY` is intentionally unset; public write/sync access starts disabled. No personal health information belongs in this app.

## Render deployment

1. In Render, create **New → Blueprint**, select the repository `harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence`, main branch.
2. Review `render.yaml` service name, starter plan, Singapore region and 1-GB disk. Confirm pricing in Render before creating.
3. Wait for the Render dashboard to show an active deployed service. Render generates the real `https://...onrender.com` URL — **do not guess it**.
4. Open `https://YOUR-ACTUAL-SERVICE.onrender.com/api/health` and confirm JSON status `ok`.
5. Open the root URL for the actual React UI. Verify indicator changes, synthetic labeling, provenance, quality page and CSV export.
6. Validate `/api/records?source=WHO` returns 0 until an authorized verified WHO import is performed.
7. Verify unauthenticated `POST /api/admin/sync-who/life_expectancy` responds 503 when admin key is not configured.
8. On a planned maintenance cycle, take and verify a SQLite backup (see [operations](OPERATIONS.md)).

## Deployment smoke test

```bash
python scripts/deployment_smoke.py --base-url https://YOUR-ACTUAL-SERVICE.onrender.com
```

The smoke test checks root HTML, health JSON, source labeling, WHO source separation and disabled sync. No personal data is sent or saved. Set an actual service URL; placeholder URLs intentionally fail.

## Optional authenticated WHO import

Live WHO data cannot be automatically declared validated solely because the endpoint returned JSON.

1. Use the manual GitHub workflow **WHO live connectivity probe** or run `python -m scripts.who_probe --country IND --indicator life_expectancy` with network access.
2. Review the actual WHO indicator metadata and its dimensions; confirm country mappings, unit, publication version and disaggregation with a domain expert. See [evidence](WHO_SOURCE_EVIDENCE.md).
3. Configure a random high-entropy `ADMIN_API_KEY` secret only in the server's private environment. Never put it in the browser, query string, repository or CI logs. Explicitly authorize the sync and closely restrict access. Re-deploy after secret changes.
4. From an authorized terminal, call the admin POST only after the probe passes. Use a full result only; the importer rejects incomplete pagination and conflicting measurements. Verify record totals and backup.
5. Expose WHO values only with correct provenance notices and caveats. Some indicators do not have verified WHO source mappings.

## Additional checks before public use

Turn on deployment alerts, uptime monitoring, rate limits at the trusted proxy or host, run a dependency/secret scan, configure a domain and HTTPS, and establish backup ownership and recovery tests. Security controls require independent review. Data/forecast models are **not validated for clinical, policy or resource-allocation decisions**.
