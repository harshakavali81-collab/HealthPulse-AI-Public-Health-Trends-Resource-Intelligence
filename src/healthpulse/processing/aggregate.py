"""Only aggregate measurements with compatible indicator units and known denominators."""
import pandas as pd

def by_year(df: pd.DataFrame):
    if df.empty:
        return []
    return (df.groupby(["indicator", "year", "unit"], as_index=False)
              .agg(value=("value", "mean"), countries=("country", "nunique"))
              .to_dict(orient="records"))
