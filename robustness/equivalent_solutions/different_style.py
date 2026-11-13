"""CORRECT, written differently from the reference: builds a list first, different key order,
pretty-printed JSON. A verifier that is too strict about form would wrongly fail this."""
import csv, json, os

APP = os.environ.get("RAINFALL_APP_DIR", "/app")

def parse(value):
    try:
        return float((value or "").strip())
    except ValueError:
        return None

with open(f"{APP}/rainfall.csv") as f:
    readings = [(r["date"], parse(r.get("rainfall_mm"))) for r in csv.DictReader(f)]
valid = [(d, mm) for d, mm in readings if mm is not None]
peak = max(mm for _, mm in valid)
report = {
    "wettest_day": next(d for d, mm in valid if mm == peak),
    "extreme_days": sum(1 for _, mm in valid if mm >= 50.0),
    "valid_readings": len(valid),
    "total_rainfall_mm": round(sum(mm for _, mm in valid), 2),
}
with open(f"{APP}/report.json", "w") as out:
    json.dump(report, out, indent=2)
