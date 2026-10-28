import pandas as pd

def compare_regions(df: pd.DataFrame, year=None):
    if df.empty:
        return []
    y = int(year) if year is not None else int(df.year.max())
    sub = df[df.year == y]
    if sub.empty:
        return []
    # Unweighted country mean. NOT a population-weighted estimate.
    result = sub.groupby("region", as_index=False).agg(value=("value", "mean"), n_countries=("country", "nunique"))
    result["value"] = result.value.round(2)
    result["year"] = y
    return result.sort_values("value", ascending=False).to_dict(orient="records")
