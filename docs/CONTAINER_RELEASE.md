# GitHub Container Registry release

The GitHub workflow [Publish tested HealthPulse Docker image](../.github/workflows/publish-container.yml) is configured to build a Docker image containing the React dashboard, FastAPI backend and the **checksum-audited 1,026-row historical World Bank WDI snapshot**. The image does not contain patient data, passwords or a valid admin key.

GitHub Actions uses its short-lived `GITHUB_TOKEN` with `packages:write` and tags each image both with `main` and an immutable `sha-<12-char-commit>` value. The job summary includes the OCI digest, which can be pinned to a deployment.

**Registry address if publishing succeeds:**

```text
ghcr.io/harshakavali81-collab/healthpulse-ai-public-health-trends-resource-intelligence:main
```

To pull and run an image **after its package is visible to your account**:

```bash
docker pull ghcr.io/harshakavali81-collab/healthpulse-ai-public-health-trends-resource-intelligence:main

docker run --rm -p 127.0.0.1:8000:8000 -e ADMIN_API_KEY= \
  -v healthpulse_data:/app/data \
  ghcr.io/harshakavali81-collab/healthpulse-ai-public-health-trends-resource-intelligence:main
```

Open `http://127.0.0.1:8000/` for the dashboard and `/api/sources` for the WDI audit totals. These commands are for **local Docker**, not a secure public deployment.

## Package privacy and hosting

Newly created packages in GitHub Container Registry may default to private, even when their source repository is public. If the image is private, the repository owner must explicitly grant access or change the package visibility; do not infer that it is public from a green workflow. When deploying externally, configure the hosting provider's registry credentials privately and pin an immutable image digest for repeatability.

Building and publishing a container **does not create a live API endpoint**. An actual public FastAPI service requires separately authorized hosting with HTTPS, secrets management, a persistent storage volume, backups and monitoring; see [Render deployment steps](DEPLOY_RENDER.md). Hosting may involve charges and must not be initiated without owner approval.

## Release verification

Every source change continues to run independent Python, frontend, Docker smoke and security checks. Registry publishing produces an image digest but **does not certify clinical safety or policy-readiness**, and is not a substitute for production monitoring.
