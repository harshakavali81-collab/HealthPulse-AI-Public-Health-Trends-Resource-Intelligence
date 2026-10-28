def quality_report(records):
    if not records:
        return {"rows": 0, "coverage": [], "duplicate_keys": 0, "missing": 0}
    seen, dups, missing = set(), 0, 0
    coverage = {}
    for r in records:
        key = (r["country"], r["indicator"], r["year"], r["source"])
        if key in seen: dups += 1
        seen.add(key)
        if r.get("value") is None: missing += 1
        coverage.setdefault(r["indicator"], set()).add(r["country"])
    return {"rows": len(records), "duplicate_keys": dups, "missing": missing,
            "coverage": [{"indicator": k, "countries": len(v)} for k, v in sorted(coverage.items())]}
