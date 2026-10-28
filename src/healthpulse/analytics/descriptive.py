import pandas as pd

def summarize(df: pd.DataFrame):
    if df.empty:
        return {"observations": 0, "countries": 0, "years": [], "indicators": 0, "latest_year": None, "latest_average": None}
    latest = int(df.year.max())
    most_recent = df[df.year == latest]
    return {
        "observations": len(df), "countries": int(df.country.nunique()),
        "years": sorted(int(y) for y in df.year.unique()), "indicators": int(df.indicator.nunique()),
        "latest_year": latest, "latest_average": round(float(most_recent.value.mean()), 2),
    }
