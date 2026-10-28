# HealthPulse AI — Verified Portfolio Release (28 October 2026)

This file distinguishes verified software artifacts from services and certifications that require external parties. **A GitHub container image is not equivalent to a running cloud API.**

## GitHub release evidence

| Component | Verified status | Evidence |
|---|---|---|
| Python application quality | **84 tests passed** | [Quality CI](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40654698790) |
| React frontend production build | **Passed** | [Quality CI](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40654698790) |
| All-in-one Docker + FastAPI health and API route smoke | **Passed** | [Deployment QA](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40654698781) |
| Security baseline workflow | **Passed** | [Security CI](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40654698737) |
| Published real historical aggregate data | **1,026 World Bank WDI observations**, 18 countries, five indicator categories | [Source manifest](../data/public/worldbank-manifest.json) |
| Real-data public portfolio browser | **Deployed and browser-tested** | [Live WDI explorer](https://harshakavali81-collab.github.io/harshavardhan-portfolio/healthpulse-worldbank.html) · [Browser QA](https://github.com/harshakavali81-collab/harshavardhan-portfolio/actions/runs/40648952963) |
| GitHub Container Registry image publication | **Succeeded** | [Container publish CI](https://github.com/harshakavali81-collab/HealthPulse-AI-Public-Health-Trends-Resource-Intelligence/actions/runs/40654698836) |
| FastAPI production cloud URL | **NOT DEPLOYED OR VERIFIED** | [Hosting steps](DEPLOY_RENDER.md) |
| WHO GHO direct live import | **NOT VERIFIED**; four checked OData routes returned HTTP 500 from a runner | [WHO diagnostic evidence](WHO_SOURCE_EVIDENCE.md) |
| Clinical, epidemiological or policy approval | **NOT OBTAINED** | [Independent validation gate](VALIDATION_PLAN.md) |

## Published container image

OCI image: `ghcr.io/harshakavali81-collab/healthpulse-ai-public-health-trends-resource-intelligence`

Commit tag: `sha-2e1c9975b4bd`

Published manifest digest:

```
sha256:878ff850d5263bc397617d83c0cde6c187cac02e10a6022fe2517cedee1217b5
```

The container registry's workflow log confirms successful pushes of both tags and the OCI digest. **Unauthenticated package visibility has not been checked.** A user may need repository/package access or to change the package's visibility before pulling it.

## Embedded WDI source integrity

The published historical WDI source manifest has this snapshot checksum:

```
sha256:3cc1ac60093f54509bce753861c03c4fccc166b15f25f56f4a5bda238fb532de
```

The Docker application validates the source checksum before startup data seeding. This proves file integrity against the repository's declared manifest; it does **not** independently certify the health-data definitions or underlying publication accuracy.

## What must still happen outside this repository?

**Public backend**: the owner must authorize a hosting account and approve any service/disk charges, configure HTTPS and a persistent storage volume, and verify an actual HTTPS endpoint against `scripts/deployment_smoke.py`. Do not invent the hostname.

**Direct WHO GHO import**: the official endpoint must become accessible from a suitable environment, return compatible data, and undergo metadata/methodology review. World Bank WDI is a **separate publisher** and must never be represented as direct WHO GHO ingestion.

**Clinical/public-policy use**: external public-health and security professionals must review the scientific methods, data representativeness, risk controls, privacy implications and jurisdiction-specific rules. No reviewer has signed off on medical/policy decisions.

## Portfolio usage

Suitable for discussing Python, SQL, FastAPI, data ingestion, analytics, React, GitHub Actions, data validation, source provenance, and deployment automation in interviews. Do not claim measured clinical benefit, production uptime, verified disease forecasts or official WHO endorsement.
