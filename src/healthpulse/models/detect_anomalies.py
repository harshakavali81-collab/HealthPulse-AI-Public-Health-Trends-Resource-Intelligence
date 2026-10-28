"""Robust z-scores on first differences, to flag jumps without classifying health risks."""
import numpy as np

def detect_anomalies(records, threshold=3.5):
    ordered = sorted(records, key=lambda r: int(r["year"]))
    if len(ordered) < 5:
        return []
    v = np.asarray([float(r["value"]) for r in ordered])
    d = np.diff(v)
    median = np.median(d)
    mad = float(np.median(np.abs(d - median)))
    if mad < 1e-9:
        return [{"year": int(ordered[i+1]["year"]), "delta": round(float(d[i]), 2), "score": None}
                for i in range(len(d)) if abs(d[i]-median) > 1e-9]
    scores = .6745 * (d - median) / mad
    return [{"year": int(ordered[i+1]["year"]), "delta": round(float(d[i]), 2), "score": round(float(scores[i]), 2)}
            for i in range(len(scores)) if abs(scores[i]) > threshold]
