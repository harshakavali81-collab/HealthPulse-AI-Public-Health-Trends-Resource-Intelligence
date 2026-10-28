"""Conservative illustrative trend projection, not a medical prediction."""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from healthpulse.processing.clean import INDICATORS

def forecast(records, indicator, horizon=3):
    if indicator not in INDICATORS:
        raise ValueError("Unknown indicator")
    if not 1 <= horizon <= 5:
        raise ValueError("Horizon must be 1-5 years")
    by_year = {int(r["year"]): float(r["value"]) for r in records}
    timeline = sorted(by_year)
    if len(timeline) < 6:
        return {"status": "insufficient_data", "message": "At least six annual observations are required", "forecast": []}
    years = np.asarray(timeline, dtype=float)
    values = np.asarray([by_year[y] for y in timeline], dtype=float)
    # Hold out the last 20% (at least two observations) to evaluate sequentially.
    test_size = max(2, int(np.ceil(len(years) * .2)))
    x = years - years[0]
    model = Ridge(alpha=2.0).fit(x[:-test_size].reshape(-1, 1), values[:-test_size])
    predicted = model.predict(x[-test_size:].reshape(-1, 1))
    baseline = np.repeat(values[-test_size-1], test_size)
    mae = float(mean_absolute_error(values[-test_size:], predicted))
    baseline_mae = float(mean_absolute_error(values[-test_size:], baseline))
    model.fit(x.reshape(-1, 1), values)
    future_years = np.arange(timeline[-1] + 1, timeline[-1] + horizon + 1, dtype=float)
    forecast_values = model.predict((future_years - years[0]).reshape(-1, 1))
    cfg = INDICATORS[indicator]
    forecast_values = np.clip(forecast_values, cfg["min"], cfg["max"])
    return {"status": "ok", "model": "Ridge linear trend", "holdout_mae": round(mae, 3),
            "baseline_mae": round(baseline_mae, 3), "validation_points": int(test_size),
            "forecast": [{"year": int(y), "value": round(float(v), 2)} for y, v in zip(future_years, forecast_values)],
            "disclaimer": "Illustrative extrapolation; forecasts are not suitable for clinical or operational decisions."}
