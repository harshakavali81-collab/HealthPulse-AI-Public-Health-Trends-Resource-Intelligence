"""Deterministic labeled synthetic example; never pass off as WHO observations."""
from random import Random
from healthpulse.processing.clean import INDICATORS

COUNTRIES = [
    ("IND", "India", "South-East Asia", 0.2),
    ("BGD", "Bangladesh", "South-East Asia", -0.15),
    ("NPL", "Nepal", "South-East Asia", -0.25),
    ("THA", "Thailand", "South-East Asia", 0.65),
    ("IDN", "Indonesia", "South-East Asia", 0.30),
    ("USA", "United States", "Americas", 1.25),
    ("BRA", "Brazil", "Americas", 0.42),
    ("MEX", "Mexico", "Americas", 0.45),
    ("CAN", "Canada", "Americas", 1.40),
    ("DEU", "Germany", "Europe", 1.45),
    ("FRA", "France", "Europe", 1.45),
    ("GBR", "United Kingdom", "Europe", 1.35),
    ("ZAF", "South Africa", "Africa", -0.40),
    ("NGA", "Nigeria", "Africa", -1.15),
    ("KEN", "Kenya", "Africa", -0.75),
    ("AUS", "Australia", "Western Pacific", 1.50),
    ("JPN", "Japan", "Western Pacific", 1.65),
    ("PHL", "Philippines", "Western Pacific", -0.10),
]

def make_demo_data():
    rng = Random(42)
    rows = []
    for code, name, region, wealth in COUNTRIES:
        for year in range(2012, 2025):
            t = year - 2012
            # Fixed random seed ensures reproducible and reviewable demo data.
            series = {
                "life_expectancy": 70 + 6*wealth + .17*t + rng.uniform(-.35,.35),
                "immunization": 79 + 9*wealth + .25*t + rng.uniform(-1.8,1.8),
                "physicians": 1.65 + 1.4*wealth + .035*t + rng.uniform(-.16,.16),
                "hospital_beds": 2.1 + 1.4*wealth + .025*t + rng.uniform(-.19,.19),
                "under5_mortality": 40 - 15*wealth - .7*t + rng.uniform(-2,2),
            }
            if code == "NGA" and year == 2020:
                series["immunization"] -= 14  # Visible anomaly for demo.
            for indicator, value in series.items():
                cfg = INDICATORS[indicator]
                rows.append({
                    "indicator": indicator, "country": code, "country_name": name,
                    "region": region, "year": year,
                    "value": round(min(cfg["max"], max(cfg["min"], value)), 2), "unit": cfg["unit"],
                    "source": "synthetic", "source_url": "", "note": "DEMO DATA — fabricated for software testing, not observed health statistics",
                })
    return rows
