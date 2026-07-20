There is a CSV of daily rainfall readings at /app/rainfall.csv. It has a header row with the columns: date, station, rainfall_mm. Each row is one day's rainfall in millimeters. Parse it and write a JSON summary to /app/report.json.

Handling of malformed rows: a row is valid only if its rainfall_mm parses as a number. Rows where rainfall_mm is empty or non-numeric must be skipped entirely — they do not count toward any statistic.

A day counts as "extreme" when its rainfall_mm is greater than or equal to 50.0.

The report must be a single JSON object with exactly these keys: total_rainfall_mm (number), valid_readings (integer), extreme_days (integer), and wettest_day (string).

Success criteria:

1. /app/report.json exists and is valid JSON.
2. valid_readings equals the number of rows whose rainfall_mm parses as a number (malformed and blank rows excluded).
3. total_rainfall_mm equals the sum of rainfall_mm across all valid rows, rounded to 2 decimal places.
4. extreme_days equals the number of valid rows whose rainfall_mm is greater than or equal to 50.0.
5. wettest_day equals the date (string) of the valid row with the highest rainfall_mm. If two or more days tie for the highest rainfall, the earliest date in file order wins.
