import csv
import json

EXTREME_THRESHOLD_MM = 50.0

total_rainfall = 0.0
valid_readings = 0
extreme_days = 0
wettest_day = None
wettest_value = -1.0

with open("/app/rainfall.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row.get("date"):
            continue
        raw = (row.get("rainfall_mm") or "").strip()
        try:
            mm = float(raw)
        except ValueError:
            # malformed or blank rainfall_mm -> skip this row entirely
            continue
        total_rainfall += mm
        valid_readings += 1
        if mm >= EXTREME_THRESHOLD_MM:
            extreme_days += 1
        # strict > keeps the first (earliest, file order) row on a tie
        if mm > wettest_value:
            wettest_value = mm
            wettest_day = row["date"]

with open("/app/report.json", "w") as out:
    json.dump(
        {
            "total_rainfall_mm": round(total_rainfall, 2),
            "valid_readings": valid_readings,
            "extreme_days": extreme_days,
            "wettest_day": wettest_day,
        },
        out,
    )
print("wrote /app/report.json")
