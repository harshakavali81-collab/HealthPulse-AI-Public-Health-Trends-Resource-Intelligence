# Power BI integration

Export the current indicator and source via **Export CSV** on the dashboard. The CSV includes indicator, country, region, year, value, unit and source for ingestion in Power BI.

Suggested Power BI measures (for a single selected indicator with consistent unit):

```dax
Mean Country Indicator = AVERAGE('Observations'[value])
Countries Reporting = DISTINCTCOUNT('Observations'[country])
Latest Reporting Year = MAX('Observations'[year])
```

Recommended visuals: (1) annual trend, (2) country map/table, (3) regional ranking, (4) coverage by year, (5) explicit provenance and unit note. Do not combine synthetic and WHO in the same measure. No `.pbix` binary is included.
