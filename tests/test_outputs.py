import csv
import json
from pathlib import Path

EXTREME_THRESHOLD_MM = 50.0


def _recompute():
    """Recompute expected values directly from /app/rainfall.csv (source of truth)."""
    total_rainfall = 0.0
    day_count = 0
    extreme_days = 0
    wettest_day = None
    wettest_value = -1.0
    with open("/app/rainfall.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("date"):
                continue
            mm = float(row["rainfall_mm"])
            total_rainfall += mm
            day_count += 1
            if mm >= EXTREME_THRESHOLD_MM:
                extreme_days += 1
            if mm > wettest_value:
                wettest_value = mm
                wettest_day = row["date"]
    return round(total_rainfall, 2), day_count, extreme_days, wettest_day


def _load_report():
    with open("/app/report.json") as f:
        return json.load(f)


def test_report_exists_and_valid_json():
    """Criterion 1: /app/report.json exists and is valid JSON."""
    assert Path("/app/report.json").exists(), "no report.json found"
    _load_report()  # raises if not valid JSON


def test_day_count():
    """Criterion 2: day_count equals the number of data rows in /app/rainfall.csv."""
    _, expected, _, _ = _recompute()
    data = _load_report()
    assert "day_count" in data, "Missing day_count"
    assert data["day_count"] == expected, f"Expected {expected}, got {data['day_count']}"


def test_total_rainfall():
    """Criterion 3: total_rainfall_mm equals the sum of rainfall_mm, rounded to 2 decimals."""
    expected, _, _, _ = _recompute()
    data = _load_report()
    assert "total_rainfall_mm" in data, "Missing total_rainfall_mm"
    assert round(float(data["total_rainfall_mm"]), 2) == expected, (
        f"Expected {expected}, got {data['total_rainfall_mm']}"
    )


def test_extreme_days():
    """Criterion 4: extreme_days equals the count of rows with rainfall_mm >= 50.0."""
    _, _, expected, _ = _recompute()
    data = _load_report()
    assert "extreme_days" in data, "Missing extreme_days"
    assert data["extreme_days"] == expected, f"Expected {expected}, got {data['extreme_days']}"


def test_wettest_day():
    """Criterion 5: wettest_day equals the date of the row with the highest rainfall_mm."""
    _, _, _, expected = _recompute()
    data = _load_report()
    assert "wettest_day" in data, "Missing wettest_day"
    assert data["wettest_day"] == expected, f"Expected {expected}, got {data['wettest_day']}"
