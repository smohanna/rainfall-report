"""WRONG: ignores the malformed-row rule. float() crashes on 'BROKEN', so no report is written."""
import csv, json, os

APP = os.environ.get("RAINFALL_APP_DIR", "/app")
total = 0.0; count = 0; extreme = 0; wettest = None; best = -1.0
with open(f"{APP}/rainfall.csv") as f:
    for row in csv.DictReader(f):
        mm = float(row["rainfall_mm"])
        total += mm; count += 1
        if mm >= 50.0: extreme += 1
        if mm > best: best, wettest = mm, row["date"]
with open(f"{APP}/report.json", "w") as out:
    json.dump({"total_rainfall_mm": round(total, 2), "valid_readings": count,
               "extreme_days": extreme, "wettest_day": wettest}, out)
