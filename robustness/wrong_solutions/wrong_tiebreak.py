"""WRONG: uses >= when tracking the maximum, so a tie resolves to the LAST day instead of the earliest.
Every other number is correct."""
import csv, json, os

APP = os.environ.get("RAINFALL_APP_DIR", "/app")
total = 0.0; count = 0; extreme = 0; wettest = None; best = -1.0
with open(f"{APP}/rainfall.csv") as f:
    for row in csv.DictReader(f):
        try:
            mm = float((row.get("rainfall_mm") or "").strip())
        except ValueError:
            continue
        total += mm; count += 1
        if mm >= 50.0: extreme += 1
        if mm >= best: best, wettest = mm, row["date"]
with open(f"{APP}/report.json", "w") as out:
    json.dump({"total_rainfall_mm": round(total, 2), "valid_readings": count,
               "extreme_days": extreme, "wettest_day": wettest}, out)
