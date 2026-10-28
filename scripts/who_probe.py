"""Manual WHO GHO connectivity and data-integrity probe. Never writes to SQLite.

Usage (from repository root):
    PYTHONPATH=src:. python -m scripts.who_probe --indicator life_expectancy --country IND
"""
from __future__ import annotations

import argparse
import json
from healthpulse.ingestion.who_loader import fetch_who_indicator


def main():
    parser=argparse.ArgumentParser(description="Check WHO GHO connection and aggregate format")
    parser.add_argument("--indicator",choices=["life_expectancy","immunization","under5_mortality"],default="life_expectancy")
    parser.add_argument("--country",default="IND",help="Three-letter WHO country code")
    parser.add_argument("--max-pages",type=int,default=10)
    options=parser.parse_args()
    result=fetch_who_indicator(options.indicator,country=options.country,max_pages=options.max_pages)
    rows=result.pop("records")
    print(json.dumps({**result,"validated_records":len(rows),
                      "years":[min(r["year"] for r in rows),max(r["year"] for r in rows)],
                      "source":"WHO GHO", "database_modified":False},indent=2))
    if result["rejected_count"]:
        raise SystemExit("Live probe detected rejected observations; verify WHO metadata before importing")


if __name__=="__main__":
    main()
