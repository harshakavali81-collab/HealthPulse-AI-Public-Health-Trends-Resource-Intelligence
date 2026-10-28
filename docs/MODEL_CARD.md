# Model card — HealthPulse AI

**Intended use:** Educational exploration of country-level annual health indicators. Not a disease forecasting, triage, diagnosis, healthcare resource-allocation or clinical model.

**Training data:** Sequential yearly observations for a single country and indicator, either clearly synthetic or imported from WHO GHO. A minimum of six annual observations is required. No individual personal records.

**Model:** Ridge regression on calendar years. The final 20% (minimum two points) are held out chronologically. MAE is reported against the holdout and against a last-training-value naive baseline. The model is refit on all years before projecting at most five additional years. Predictions are clipped to feasible units.

**Anomalies:** Median absolute deviation on year-to-year changes; flags are data-review candidates, not outbreak detections. Clustering: standardized latest values for complete-country/indicator matrix, KMeans seeded at 42.

**Key limitations:** Annual irregularities, revision cycles, coverage differences, denominator shifts, missingness, intervention effects, nonlinearity and demographic differences are unmodeled. The model does not produce reliable calibrated prediction intervals. It should not be used in emergency response, individual patient risk, resource procurement, or policy decisions without expert validation.

**Monitoring proposal:** Check source updates, data coverage, schema drift, units, missingness, changes of indicator codes, forecast holdout errors and stale cache age. The demo version does not implement automated scheduled ingestion or drift alerts.
