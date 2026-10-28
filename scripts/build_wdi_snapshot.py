"""Build a source-audited *real* World Bank WDI historical snapshot.

This is a manually/CI-triggered operation, not server startup. No patient-level
information is accepted; records are public country-year aggregates. A partial
fetch causes nonzero exit and no new published snapshot.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import tempfile
from healthpulse.ingestion.worldbank_loader import DEFAULT_COUNTRIES, WB_CODES, fetch_worldbank_indicator


def build_snapshot(fetcher=fetch_worldbank_indicator) -> dict:
    records = []
    manifest = []
    for indicator in WB_CODES:
        batch = fetcher(indicator, countries=DEFAULT_COUNTRIES)
        if not batch.get("complete"):
            raise RuntimeError(f"Unverified or incomplete WDI batch: {indicator}")
        rows = batch["records"]
        if not rows or any(r.get("source") != "WorldBank" or r["indicator"] != indicator for r in rows):
            raise RuntimeError(f"Missing/incorrect WDI rows for {indicator}")
        records.extend(rows)
        manifest.append({
            "indicator": indicator,
            "worldbank_code": WB_CODES[indicator],
            "rows": len(rows),
            "countries_with_data": batch["countries_with_data"],
            "fetched_at_utc": batch["fetched_at_utc"],
        })
    keys = [(r["country"], r["indicator"], r["year"], r["source"]) for r in records]
    if len(keys) != len(set(keys)):
        raise RuntimeError("Duplicate country-year indicator records in snapshot")
    records.sort(key=lambda x: (x["indicator"], x["country"], x["year"]))
    return {
        "schema_version": "1.0",
        "publisher": "World Bank World Development Indicators (WDI)",
        "source": "WorldBank",
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_documentation": "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392",
        "license": "CC BY 4.0 - World Bank WDI, original underlying providers credited by indicator metadata",
        "purpose": "Educational country-level exploration; not clinical, policy or resource-allocation guidance",
        "scope": {"countries_requested": list(DEFAULT_COUNTRIES), "years_requested": [2012, 2024]},
        "indicator_manifest": manifest,
        "records": records,
    }


def serialize_snapshot(snapshot):
    data=json.dumps(snapshot, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    summary={
        "source":"WorldBank", "publisher":snapshot["publisher"],
        "source_fetched_at_utc":snapshot["fetched_at_utc"],
        "rows":len(snapshot["records"]), "countries":len({r["country"] for r in snapshot["records"]}),
        "indicators":snapshot["indicator_manifest"],
        "snapshot_sha256": hashlib.sha256(data).hexdigest(),
        "license":snapshot["license"], "methodological_status":"not clinically or policy validated",
    }
    header=("indicator","country","country_name","region","year","value","unit","source","source_url","note")
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream, fieldnames=header, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in snapshot["records"]:
        # Protect spreadsheet users from CSV formula injection.
        clean=dict(row)
        for field in header:
            value=clean.get(field)
            if isinstance(value,str) and value.startswith(("=","+","-","@","\t","\r")):
                clean[field]="'"+value
        writer.writerow(clean)
    return data, json.dumps(summary, indent=2).encode("utf-8") + b"\n", stream.getvalue().encode("utf-8")


def publish_snapshot(snapshot, directory: Path):
    payloads=serialize_snapshot(snapshot)
    names=("worldbank-wdi-2012-2024.json", "worldbank-manifest.json", "worldbank-wdi-2012-2024.csv")
    directory.mkdir(parents=True, exist_ok=True)
    temporary=[]
    try:
        for filename, payload in zip(names, payloads):
            with tempfile.NamedTemporaryFile(dir=directory, prefix=".wdi-", delete=False) as handle:
                handle.write(payload)
                temporary.append((Path(handle.name), directory / filename))
        for tmp, target in temporary:
            tmp.replace(target)
    finally:
        for tmp,_ in temporary:
            tmp.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=Path("data/public"))
    args=parser.parse_args()
    snapshot=build_snapshot()
    publish_snapshot(snapshot,args.out)
    print(json.dumps({"status":"verified WDI snapshot created","rows":len(snapshot["records"]),
                      "indicators":len(snapshot["indicator_manifest"]),
                      "output":str(args.out)}, indent=2))


if __name__=="__main__":
    main()
