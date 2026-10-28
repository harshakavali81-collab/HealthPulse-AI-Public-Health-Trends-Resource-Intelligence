# World Bank public historical snapshot (generated, never synthetic)

A dedicated [GitHub Actions workflow](../../.github/workflows/worldbank-snapshot.yml) fetches five official World Bank WDI public indicator series across the 18 configured country codes and 2012–2024 (availability differs by source). It validates every series before saving anything, and fails the build if a series is incomplete, source metadata is inconsistent, or an invalid number would enter the dataset.

### Output assets

Once the workflow succeeds, `data/public/` contains:

- `worldbank-wdi-2012-2024.json`: country-year value records with publisher, fetch timestamp, indicator labels, source URL, WDI provenance and source caveats.
- `worldbank-manifest.json`: observation counts per indicator and a SHA-256 checksum of the JSON.
- `worldbank-wdi-2012-2024.csv`: spreadsheet-friendly export, with formula injection protection.

The workflow both uploads these as a downloadable artifact and attempts to commit them to `main`. GitHub repository workflow permissions must permit `contents: write`; if permissions prevent the push, the artifact remains available in the workflow run, and the repository should not claim a snapshot was published.

### Data governance

- **Real public country-level aggregates only.** Not individual medical records.
- **Provider is World Bank WDI**, NOT a direct WHO GHO import. Re-exported source attribution and original producer metadata must be checked for scientific reporting.
- Covers a fixed historical window; the dataset is not real-time disease surveillance.
- Missing values, unavailable years and provider estimate revisions remain limitations.
- Data are licensed under World Bank terms (commonly CC BY 4.0); provide appropriate attribution to the World Bank and originating data producers.
- A successful data-fetch process is not clinical or policy validation.

To refresh the snapshot manually, open Actions → **Publish audited World Bank public snapshot** → Run workflow, or run:
```bash
PYTHONPATH=src:. python -m scripts.build_wdi_snapshot --out data/public
```
