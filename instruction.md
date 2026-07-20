There is a CSV of daily rainfall readings at /app/rainfall.csv. It has a header row with the columns: date, station, rainfall_mm. Each row is one day's rainfall in millimeters. Parse it and write a JSON summary to /app/report.json.

A day counts as "extreme" when its rainfall_mm is greater than or equal to 50.0.

The report must be a single JSON object with exactly these keys: total_rainfall_mm (number), day_count (integer), extreme_days (integer), and wettest_day (string).

Success criteria:

1. /app/report.json exists and is valid JSON.
2. day_count equals the number of data rows in /app/rainfall.csv (excluding the header, excluding blank lines).
3. total_rainfall_mm equals the sum of rainfall_mm across all data rows, rounded to 2 decimal places.
4. extreme_days equals the number of rows whose rainfall_mm is greater than or equal to 50.0.
5. wettest_day equals the date (string) of the row with the highest rainfall_mm.
