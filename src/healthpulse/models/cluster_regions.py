"""Exploratory clustering; never used to allocate healthcare resources."""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_countries(df: pd.DataFrame, n_clusters=3):
    if df.empty:
        return []
    # Latest available year per country + indicator; require same indicators for all clusters.
    latest = df.sort_values("year").drop_duplicates(["country", "indicator"], keep="last")
    matrix = latest.pivot(index="country", columns="indicator", values="value")
    matrix = matrix.dropna()
    if len(matrix) < max(3, n_clusters):
        return []
    x = StandardScaler().fit_transform(matrix.values)
    km = KMeans(n_clusters=n_clusters, n_init=10, random_state=42).fit(x)
    return [{"country": country, "cluster": int(cluster)} for country, cluster in zip(matrix.index, km.labels_)]
