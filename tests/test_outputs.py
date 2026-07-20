import csv
import json
from pathlib import Path

EXTREME_THRESHOLD_MM = 50.0


def _recompute():
    """Recompute expected values directly from /app/rainfall.csv (source of truth).

    Mirrors the instruction's rules: malformed/blank rainfall_mm rows are skipped;
    ties for the wettest day are broken by earliest file order (strict >).
    """
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
                continue
            total_rainfall += mm
            valid_readings += 1
            if mm >= EXTREME_THRESHOLD_MM:
                extreme_days += 1
            if mm > wettest_value:
                wettest_value = mm
                wettest_day = row["date"]
    return round(total_rainfall, 2), valid_readings, extreme_days, wettest_day


def _load_report():
    with open("/app/report.json") as f:
        return json.load(f)


def test_report_exists_and_valid_json():
    """Criterion 1: /app/report.json exists and is valid JSON."""
    assert Path("/app/report.json").exists(), "no report.json found"
    _load_report()  # raises if not valid JSON


def test_valid_readings_excludes_malformed():
    """Criterion 2: valid_readings counts only rows whose rainfall_mm parses as a number."""
    _, expected, _, _ = _recompute()
    data = _load_report()
    assert "valid_readings" in data, "Missing valid_readings"
    assert data["valid_readings"] == expected, (
        f"Expected {expected}, got {data['valid_readings']}"
    )


def test_total_rainfall():
    """Criterion 3: total_rainfall_mm sums only valid rows, rounded to 2 decimals."""
    expected, _, _, _ = _recompute()
    data = _load_report()
    assert "total_rainfall_mm" in data, "Missing total_rainfall_mm"
    assert round(float(data["total_rainfall_mm"]), 2) == expected, (
        f"Expected {expected}, got {data['total_rainfall_mm']}"
    )


def test_extreme_days():
    """Criterion 4: extreme_days counts valid rows with rainfall_mm >= 50.0."""
    _, _, expected, _ = _recompute()
    data = _load_report()
    assert "extreme_days" in data, "Missing extreme_days"
    assert data["extreme_days"] == expected, (
        f"Expected {expected}, got {data['extreme_days']}"
    )


def test_wettest_day_tie_breaks_to_earliest():
    """Criterion 5: wettest_day is the highest rainfall row; ties break to earliest file order."""
    _, _, _, expected = _recompute()
    data = _load_report()
    assert "wettest_day" in data, "Missing wettest_day"
    assert data["wettest_day"] == expected, (
        f"Expected {expected}, got {data['wettest_day']}"
    )
