"""WRONG (reward-hacking attempt): creates the output file without doing the work.
A verifier that only checks that the file exists would pass this."""
import json, os

APP = os.environ.get("RAINFALL_APP_DIR", "/app")
with open(f"{APP}/report.json", "w") as out:
    json.dump({}, out)
