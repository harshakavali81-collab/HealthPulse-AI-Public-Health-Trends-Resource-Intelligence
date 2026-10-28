# HealthPulse data and image release gates

## Audited data and release safeguards

The historical WDI snapshot is checked against its SHA-256 manifest **and** against every stored SQLite row when the source is already managed. If its local data were accidentally modified or partly deleted, startup restores the complete validated historical snapshot transactionally instead of reporting a misleading successful integrity check. The WHO loader refuses incomplete pages, contradictory observations and **invalid total-population aggregate rows**.

The GitHub Container Registry publishing job now **requires a passing Python test suite, snapshot checksum verification and React production build** before an image can be pushed. The complete Docker runtime smoke test remains a separate mandatory human-reviewed check before public deployment; passing CI is not a certification.


## Controlled lifecycle

1. A separate approved workflow obtains aggregate World Bank WDI data and writes its checksum manifest.
2. Container startup verifies source labels, SHA-256, record/indicator counts and each row's schema.
3. A pinned SQLite source is compared row-for-row to the verified source before startup declares it unchanged; tampering or missing observations are repaired from the committed historical snapshot.
4. WHO GHO imports fail closed when a total-population record is invalid or pagination is truncated. The upstream service was observed returning HTTP 500 from a GitHub runner on 28 October 2026 and direct WHO import remains unverified.
5. Docker image publishing is gated on Python unit tests, the source snapshot check and a React build.
6. Operators review the separate Docker smoke results, release digest and application security prior to any public backend deployment.
7. External epidemiological and regulatory approval is required before clinical or policy use.

## Boundaries

The real-data portfolio site is a **static historical** WDI explorer, not a live WHO portal. Docker images in GitHub Container Registry are release artifacts, not hosted servers. Render Blueprint hosting requires the owner's explicit service and payment authorization; no Render URL is claimed.
