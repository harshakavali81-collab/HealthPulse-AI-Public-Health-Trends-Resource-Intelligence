# Independent validation and public-health safety gate

**Status: NOT CLINICALLY OR POLICY VALIDATED.** HealthPulse is an educational research and portfolio tool for aggregate indicators. Automated tests demonstrate software correctness for fixtures; they do not constitute epidemiological validation, a medical-device assessment or WHO endorsement.

| Gate | Required evidence | Current status |
|---|---|---|
| Source integrity | Verify exact WHO indicator definitions, codes, units, dimension filters, country labels, publication/revision timestamps | Documentation checked in part; live import unverified |
| Scope | Restrict to aggregate non-personal observations; privacy threat-model | Demo has only aggregates; external independent review pending |
| Data quality | Independent checks of missingness, duplicate sources, denominator shifts, year comparability and data licenses | Programmatic checks available; domain review pending |
| Trends | Quantify sensitivity to reporting gaps, revisions and external changes | Not independently validated |
| Forecast evaluation | Multi-country time-based holdouts, calibration and drift evaluation; explicit abstention policy | Ridge vs naive exploratory baseline only |
| Clustering & anomalies | Review spurious clusters and change-point interpretation for different data densities | Exploratory, unvalidated |
| Resource use | Establish population-weighted, service-reach, capacity and equity evidence | Not permitted by current prototype |
| Ethics & governance | Expert epidemiologist, statistician and security assessor sign off; ethics and regulatory assessment if warranted | **No sign-off** |
| Operational | Public HTTPS smoke test, backups, privacy review, incident response, production security | Blueprint ready; deployment and external review pending |

## Reviewer sign-off (blank until actually performed)

- Epidemiology reviewer and affiliation: **NOT ASSIGNED**
- Statistical review: **NOT ASSIGNED**
- Privacy and security review: **NOT ASSIGNED**
- Jurisdiction-specific compliance determination: **NOT ASSESSED**
- Written approval/decision: **NOT GRANTED**

## Go / no-go rule

No release may claim clinical safety, patient-level prediction, outbreak detection, verified resource gaps or policy recommendation without independent domain evidence and approval. An educational public prototype with strong synthetic labels may be distributed without claiming these uses. External WHO public aggregates do not eliminate methodology or governance requirements.
