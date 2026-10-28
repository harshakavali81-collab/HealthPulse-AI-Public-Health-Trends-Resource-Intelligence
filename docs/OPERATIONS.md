# Backup, restore and operations

HealthPulse uses a SQLite file in the named Docker volume `healthpulse_data` by default. No patient data belongs in this database. Backups are intentionally **not** committed to GitHub.

## Integrity validation

From a local source checkout with Python installed:

```bash
python scripts/db_maintenance.py verify --database data/healthpulse.db
```

The verifier uses read-only SQLite access and reports source counts and `PRAGMA integrity_check`. It fails if the database is missing or does not contain the expected HealthPulse observations table.

## Transactionally consistent backup

```bash
python scripts/db_maintenance.py backup --database data/healthpulse.db --output backups/healthpulse-2026-10-28.sqlite
```

The backup uses SQLite's online `backup` API and an atomic destination rename. It refuses to overwrite an existing file and verifies integrity before publishing the result.

For Docker Compose, the database resides in the named volume and is **not** at `./data/healthpulse.db` on your host. Use the following copy workflow:

```bash
docker compose exec -T api python -m scripts.db_maintenance verify --database /app/data/healthpulse.db
docker compose exec -T api python -m scripts.db_maintenance backup --database /app/data/healthpulse.db --output /app/data/healthpulse-backup.sqlite
docker compose cp api:/app/data/healthpulse-backup.sqlite ./healthpulse-backup.sqlite
```

`scripts/` is included in the API Docker image. Store backup files offsite with appropriate access controls; keep at least one verified recovery copy.

## Restore safely

1. Stop writes: `docker compose down` (do not use `-v`, which deletes volumes).
2. Keep a separate copy of the current database, and verify the candidate restore using the CLI.
3. Replace the SQLite volume file using a temporary maintenance container with the volume mounted. Do not overwrite a running SQLite database or discard its WAL files while the API is active.
4. Restart `docker compose up -d` and inspect `/api/health`, `/api/quality`, and each source's record counts.

Exact volume-mount commands differ by Docker platform; this guide deliberately avoids an unsafe one-line overwrite.

## Operations checklist

- Keep the Docker dashboard behind HTTPS and enforce authorization on external writes.
- Leave `ADMIN_API_KEY` unset unless intentional WHO imports are required.
- Before WHO imports, verify indicator code, WHO terms of use, units, dimensions, geographies and years.
- Check source counts, country-year gaps, provenance and quality monitoring before presenting numbers.
- Run GitHub CI and smoke tests after every change.
- The public GitHub Pages real-data explorer uses a separately hosted, source-labeled historical World Bank WDI aggregate snapshot; the synthetic demonstration is labeled separately. Neither is the cloud-hosted FastAPI service.

## Managing the published World Bank snapshot

Bundled World Bank records are verified against their SHA-256 manifest at startup when `HEALTHPULSE_AUTOLOAD_WDI=1`. The data remains historical, not a live feed. Do not call per-indicator admin sync against a managed snapshot: the API deliberately returns HTTP 409 to prevent unreviewed overrides and misleading provenance. To update the published record set, use the dedicated source-audited GitHub snapshot publishing workflow and release the resulting complete dataset together with its manifest, then review the new counts and data definitions before deployment.

## Liveness versus readiness

`GET /api/health` reports process **liveness**. Docker and Render now monitor `GET /api/ready` for SQLite **readiness**: the database must exist, pass SQLite quick-check and contain consistent managed source record counts. Readiness uses a read-only SQLite connection and returns HTTP 503 for a missing or inconsistent database; it never creates one. It is **not** a substitute for independent epidemiological or source-methodology validation.
