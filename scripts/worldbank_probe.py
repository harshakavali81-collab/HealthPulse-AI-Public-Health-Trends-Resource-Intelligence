"""Read-only World Bank API probe. Does not modify SQLite."""
import argparse
import json
from healthpulse.ingestion.worldbank_loader import fetch_worldbank_indicator, WB_CODES


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--indicator",choices=sorted(WB_CODES),default="life_expectancy")
    parser.add_argument("--country",default="IND",help="Single ISO3 country for bounded probe")
    args=parser.parse_args()
    batch=fetch_worldbank_indicator(args.indicator,countries=(args.country,),max_pages=3)
    rows=batch.pop("records")
    print(json.dumps({**batch,"preview":rows[-3:],
                      "database_modified":False,"clinical_validation":False},indent=2))


if __name__=="__main__":
    main()
