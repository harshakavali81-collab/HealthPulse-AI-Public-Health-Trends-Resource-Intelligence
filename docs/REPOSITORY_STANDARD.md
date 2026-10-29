# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`Dockerfile`](<../Dockerfile>)
- [`Dockerfile.deploy`](<../Dockerfile.deploy>)
- [`README.md`](<../README.md>)
- [`assets`](<../assets>)
- [`assets/coverage-example.png`](<../assets/coverage-example.png>)
- [`assets/dashboard-preview.png`](<../assets/dashboard-preview.png>)
- [`assets/diagrams`](<../assets/diagrams>)
- [`assets/diagrams/01-system-architecture.svg`](<../assets/diagrams/01-system-architecture.svg>)
- [`assets/diagrams/02-ingestion-pipeline.svg`](<../assets/diagrams/02-ingestion-pipeline.svg>)
- [`assets/diagrams/03-project-workflow.svg`](<../assets/diagrams/03-project-workflow.svg>)
- [`assets/diagrams/04-observation-schema.svg`](<../assets/diagrams/04-observation-schema.svg>)
- [`assets/diagrams/05-forecast-evaluation.svg`](<../assets/diagrams/05-forecast-evaluation.svg>)
- [`assets/diagrams/06-api-data-lifecycle.svg`](<../assets/diagrams/06-api-data-lifecycle.svg>)
- [`assets/diagrams/07-project-tree.svg`](<../assets/diagrams/07-project-tree.svg>)
- [`assets/real-data`](<../assets/real-data>)
- [`assets/real-data/01-life-expectancy.svg`](<../assets/real-data/01-life-expectancy.svg>)
- [`assets/real-data/02-dtp3-immunization.svg`](<../assets/real-data/02-dtp3-immunization.svg>)
- [`assets/real-data/03-under-five-mortality.svg`](<../assets/real-data/03-under-five-mortality.svg>)
- [`assets/real-data/04-country-indicator-coverage.svg`](<../assets/real-data/04-country-indicator-coverage.svg>)
- [`assets/trend-example.png`](<../assets/trend-example.png>)
- [`backend`](<../backend>)
- [`backend/__init__.py`](<../backend/__init__.py>)
- [`backend/app`](<../backend/app>)
- [`backend/app/__init__.py`](<../backend/app/__init__.py>)
- [`backend/app/db`](<../backend/app/db>)
- [`backend/app/db/__init__.py`](<../backend/app/db/__init__.py>)
- [`backend/app/db/store.py`](<../backend/app/db/store.py>)
- [`backend/app/main.py`](<../backend/app/main.py>)
- [`backend/app/routes`](<../backend/app/routes>)
- [`backend/app/routes/__init__.py`](<../backend/app/routes/__init__.py>)
- [`data`](<../data>)
- [`data/README.md`](<../data/README.md>)
- [`data/public`](<../data/public>)
- [`data/public/worldbank-manifest.json`](<../data/public/worldbank-manifest.json>)
- [`data/public/worldbank-wdi-2012-2024.csv`](<../data/public/worldbank-wdi-2012-2024.csv>)
- [`data/public/worldbank-wdi-2012-2024.json`](<../data/public/worldbank-wdi-2012-2024.json>)
- [`docker-compose.yml`](<../docker-compose.yml>)
- [`docs`](<../docs>)
- [`docs/ARCHITECTURE.md`](<../docs/ARCHITECTURE.md>)
- [`docs/CONTAINER_RELEASE.md`](<../docs/CONTAINER_RELEASE.md>)
- [`docs/DATA_DICTIONARY.md`](<../docs/DATA_DICTIONARY.md>)
- [`docs/DATA_RELEASE_GATES.md`](<../docs/DATA_RELEASE_GATES.md>)
- [`docs/DEPLOY_RENDER.md`](<../docs/DEPLOY_RENDER.md>)
- [`docs/MODEL_CARD.md`](<../docs/MODEL_CARD.md>)
- [`docs/OPERATIONS.md`](<../docs/OPERATIONS.md>)
- [`docs/PORTFOLIO_CASE_STUDY.md`](<../docs/PORTFOLIO_CASE_STUDY.md>)
- [`docs/PROJECT_TREE.txt`](<../docs/PROJECT_TREE.txt>)
- [`docs/REAL_WDI_VISUALS.md`](<../docs/REAL_WDI_VISUALS.md>)
- [`docs/RELEASE_STATUS.md`](<../docs/RELEASE_STATUS.md>)
- [`docs/SECURITY.md`](<../docs/SECURITY.md>)
- [`docs/VALIDATION_PLAN.md`](<../docs/VALIDATION_PLAN.md>)
- [`docs/VISUAL_GALLERY.md`](<../docs/VISUAL_GALLERY.md>)
- [`docs/WDI_SNAPSHOT.md`](<../docs/WDI_SNAPSHOT.md>)
- [`docs/WHO_SOURCE_EVIDENCE.md`](<../docs/WHO_SOURCE_EVIDENCE.md>)
- [`docs/WORKFLOWS.md`](<../docs/WORKFLOWS.md>)
- [`docs/WORLDBANK_SOURCE.md`](<../docs/WORLDBANK_SOURCE.md>)
- [`frontend`](<../frontend>)
- [`frontend/Dockerfile`](<../frontend/Dockerfile>)
- [`frontend/index.html`](<../frontend/index.html>)
- [`frontend/nginx.conf`](<../frontend/nginx.conf>)
- [`frontend/package.json`](<../frontend/package.json>)
- [`frontend/src`](<../frontend/src>)
- [`frontend/src/api`](<../frontend/src/api>)
- [`frontend/src/api/client.js`](<../frontend/src/api/client.js>)
- [`frontend/src/components`](<../frontend/src/components>)
- [`frontend/src/components/Charts.jsx`](<../frontend/src/components/Charts.jsx>)
- [`frontend/src/main.jsx`](<../frontend/src/main.jsx>)
- [`frontend/src/pages`](<../frontend/src/pages>)
- [`frontend/src/pages/DataProvenance.jsx`](<../frontend/src/pages/DataProvenance.jsx>)
- [`frontend/src/pages/Indicators.jsx`](<../frontend/src/pages/Indicators.jsx>)
- [`frontend/src/pages/Overview.jsx`](<../frontend/src/pages/Overview.jsx>)
- [`frontend/src/pages/QualityMonitoring.jsx`](<../frontend/src/pages/QualityMonitoring.jsx>)
- [`frontend/src/pages/RegionalComparison.jsx`](<../frontend/src/pages/RegionalComparison.jsx>)
- [`frontend/src/pages/ResourceContext.jsx`](<../frontend/src/pages/ResourceContext.jsx>)
- [`frontend/src/pages/Trends.jsx`](<../frontend/src/pages/Trends.jsx>)
- [`frontend/src/styles.css`](<../frontend/src/styles.css>)
- [`frontend/vite.config.js`](<../frontend/vite.config.js>)
- [`notebooks`](<../notebooks>)
- [`notebooks/01_indicator_exploration.ipynb`](<../notebooks/01_indicator_exploration.ipynb>)
- [`notebooks/02_region_comparison.ipynb`](<../notebooks/02_region_comparison.ipynb>)
- [`notebooks/03_trend_forecasting.ipynb`](<../notebooks/03_trend_forecasting.ipynb>)
- [`portfolio`](<../portfolio>)
- [`portfolio/PORTFOLIO_CARD.md`](<../portfolio/PORTFOLIO_CARD.md>)
- [`portfolio/README.md`](<../portfolio/README.md>)
- [`portfolio/healthpulse-case-study.html`](<../portfolio/healthpulse-case-study.html>)
- [`portfolio/healthpulse-demo.html`](<../portfolio/healthpulse-demo.html>)
- [`portfolio/healthpulse-worldbank.html`](<../portfolio/healthpulse-worldbank.html>)
- [`powerbi`](<../powerbi>)
- [`powerbi/README.md`](<../powerbi/README.md>)
- [`render.yaml`](<../render.yaml>)
- [`requirements.txt`](<../requirements.txt>)
- [`scripts`](<../scripts>)
- [`scripts/__init__.py`](<../scripts/__init__.py>)
- [`scripts/build_wdi_snapshot.py`](<../scripts/build_wdi_snapshot.py>)
- [`scripts/db_maintenance.py`](<../scripts/db_maintenance.py>)
- [`scripts/deployment_smoke.py`](<../scripts/deployment_smoke.py>)
- [`scripts/who_diagnostics.py`](<../scripts/who_diagnostics.py>)
- [`scripts/who_probe.py`](<../scripts/who_probe.py>)
- [`scripts/worldbank_probe.py`](<../scripts/worldbank_probe.py>)
- [`src`](<../src>)
- [`src/healthpulse`](<../src/healthpulse>)
- [`src/healthpulse/__init__.py`](<../src/healthpulse/__init__.py>)
- [`src/healthpulse/analytics`](<../src/healthpulse/analytics>)
- [`src/healthpulse/analytics/descriptive.py`](<../src/healthpulse/analytics/descriptive.py>)
- [`src/healthpulse/analytics/regional_comparison.py`](<../src/healthpulse/analytics/regional_comparison.py>)
- [`src/healthpulse/ingestion`](<../src/healthpulse/ingestion>)
- [`src/healthpulse/ingestion/public_dataset_loader.py`](<../src/healthpulse/ingestion/public_dataset_loader.py>)
- [`src/healthpulse/ingestion/published_snapshot.py`](<../src/healthpulse/ingestion/published_snapshot.py>)
- [`src/healthpulse/ingestion/who_loader.py`](<../src/healthpulse/ingestion/who_loader.py>)
- [`src/healthpulse/ingestion/worldbank_loader.py`](<../src/healthpulse/ingestion/worldbank_loader.py>)
- [`src/healthpulse/models`](<../src/healthpulse/models>)
- [`src/healthpulse/models/cluster_regions.py`](<../src/healthpulse/models/cluster_regions.py>)
- [`src/healthpulse/models/detect_anomalies.py`](<../src/healthpulse/models/detect_anomalies.py>)
- [`src/healthpulse/models/forecast.py`](<../src/healthpulse/models/forecast.py>)
- [`src/healthpulse/monitoring`](<../src/healthpulse/monitoring>)
- [`src/healthpulse/monitoring/quality.py`](<../src/healthpulse/monitoring/quality.py>)
- [`src/healthpulse/processing`](<../src/healthpulse/processing>)
- [`src/healthpulse/processing/aggregate.py`](<../src/healthpulse/processing/aggregate.py>)
- [`src/healthpulse/processing/clean.py`](<../src/healthpulse/processing/clean.py>)
- [`src/healthpulse/processing/validate.py`](<../src/healthpulse/processing/validate.py>)
- [`tests`](<../tests>)
- [`tests/conftest.py`](<../tests/conftest.py>)
- [`tests/test_analytics.py`](<../tests/test_analytics.py>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_deployment_smoke.py`](<../tests/test_deployment_smoke.py>)
- [`tests/test_maintenance.py`](<../tests/test_maintenance.py>)
- [`tests/test_processing.py`](<../tests/test_processing.py>)
- [`tests/test_published_snapshot.py`](<../tests/test_published_snapshot.py>)
- [`tests/test_readiness.py`](<../tests/test_readiness.py>)
- [`tests/test_release_safeguards.py`](<../tests/test_release_safeguards.py>)
- [`tests/test_wdi_snapshot.py`](<../tests/test_wdi_snapshot.py>)
- [`tests/test_who_loader.py`](<../tests/test_who_loader.py>)
- [`tests/test_worldbank_loader.py`](<../tests/test_worldbank_loader.py>)
