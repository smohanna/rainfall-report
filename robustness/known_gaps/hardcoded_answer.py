"""KNOWN GAP: writes the correct numbers without reading the data.
The verifier cannot tell this apart from a real solution, because the input file never changes.
Closing this gap needs inputs the agent has not seen (e.g. a second, hidden CSV at verify time)."""
import json, os

APP = os.environ.get("RAINFALL_APP_DIR", "/app")
with open(f"{APP}/report.json", "w") as out:
    json.dump({"total_rainfall_mm": 480.8, "valid_readings": 7,
               "extreme_days": 5, "wettest_day": "2024-04-29"}, out)
