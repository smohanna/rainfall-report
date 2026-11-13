#!/usr/bin/env python3
"""Stress-test the verifier (tests/test_outputs.py) against solutions with a known verdict.

oracle and nop only cover the two extremes: a fully correct solution and no solution.
This script covers the space in between. For each candidate solution it builds a throwaway
copy of the task environment, runs the solution, runs the real verifier, and compares the
verdict with the one we expect:

  solution/solve.py             reference solution        -> must PASS
  equivalent_solutions/*.py     correct, different style  -> must PASS
  wrong_solutions/*.py          wrong or cheating         -> must FAIL
  known_gaps/*.py               wrong, but not detected   -> PASS today (documented limits)

No Docker needed:  python3 robustness/check_verifier.py
Exit code is 0 only if every verdict matches the expectation.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "robustness"


def verdict(solution: Path) -> tuple[str, str]:
    """Run one solution plus the verifier in a fresh temp dir. Returns (PASS|FAIL, detail)."""
    with tempfile.TemporaryDirectory() as tmp:
        app = Path(tmp) / "app"
        app.mkdir()
        shutil.copy(ROOT / "environment" / "rainfall.csv", app / "rainfall.csv")

        # The task files hardcode /app (the path inside the container). Point copies at the temp dir.
        code = solution.read_text().replace('"/app/', f'"{app}/')
        runnable = Path(tmp) / "solution.py"
        runnable.write_text(code)
        tests = Path(tmp) / "test_outputs.py"
        tests.write_text((ROOT / "tests" / "test_outputs.py").read_text().replace("/app/", f"{app}/"))

        env = {**os.environ, "RAINFALL_APP_DIR": str(app)}
        run = subprocess.run([sys.executable, str(runnable)], env=env, capture_output=True, text=True)
        crashed = run.returncode != 0

        check = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests), "-q", "--no-header", "-p", "no:cacheprovider"],
            capture_output=True, text=True,
            env={**os.environ, "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        )
        failed = [line.split("::")[1].split(" ")[0] for line in check.stdout.splitlines()
                  if line.startswith("FAILED")]
        if check.returncode == 0:
            return "PASS", "all criteria met"
        detail = f"{len(failed)} of 5 tests failed"
        if len(failed) == 1:
            detail = f"caught by {failed[0]}"
        if crashed:
            detail = "solution crashed; " + detail
        return "FAIL", detail


def main() -> int:
    groups = [
        ("Reference solution", [ROOT / "solution" / "solve.py"], "PASS"),
        ("Correct, written differently", sorted((HERE / "equivalent_solutions").glob("*.py")), "PASS"),
        ("Wrong or cheating", sorted((HERE / "wrong_solutions").glob("*.py")), "FAIL"),
        ("Known gaps (wrong, not detected)", sorted((HERE / "known_gaps").glob("*.py")), "PASS"),
    ]
    mismatches = 0
    for title, files, expected in groups:
        print(f"\n{title} (expected: {expected})")
        for f in files:
            got, detail = verdict(f)
            ok = got == expected
            mismatches += not ok
            print(f"  {'ok ' if ok else 'BAD'} {f.name:<24} {got:<5} {detail}")
    print()
    if mismatches:
        print(f"{mismatches} verdict(s) did not match the expectation.")
        return 1
    print("Every verdict matches the expectation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
