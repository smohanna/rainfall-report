# rainfall-report — an AI-agent evaluation task for extreme-rainfall data

A self-authored **evaluation task** for AI coding agents, in the Terminal-Bench 2
(Harbor) format, applied to a climate problem: turning a CSV of daily rainfall
readings into a JSON summary that flags extreme-rain days.

The point of this repo isn't the ETL — it's the **evaluation**. As AI agents take
on real work with climate and weather data, we need tasks that measure whether an
agent *actually* produced the right numbers, in an environment that runs the same
way everywhere. This is a compact, honestly-graded example of exactly that — and
it deliberately includes messy-data edge cases so the verifier discriminates
*correct* solutions from *almost-correct* ones.

> Self-authored with synthetic data. Independent portfolio work — not affiliated
> with or derived from any employer or organization.

## What the task asks

Given `/app/rainfall.csv` (columns: `date, station, rainfall_mm`), produce
`/app/report.json` with exactly:

| key                 | type    | meaning                                              |
| ------------------- | ------- | ---------------------------------------------------- |
| `total_rainfall_mm` | number  | sum of `rainfall_mm` over valid rows, rounded 2 dp   |
| `valid_readings`    | integer | rows whose `rainfall_mm` parses as a number          |
| `extreme_days`      | integer | valid rows with `rainfall_mm >= 50.0`                |
| `wettest_day`       | string  | `date` of the highest-rainfall valid row             |

## The edge cases (what makes this more than trivial parsing)

The input data is intentionally messy, and the instruction specifies exactly how
to handle it — so the task tests judgment, not just a loop:

- **Malformed / blank readings.** Some `rainfall_mm` cells are empty or
  non-numeric (e.g. `BROKEN`). Valid rows are only those that parse as a number;
  malformed rows are skipped and count toward nothing. A naive solution that does
  `float(row["rainfall_mm"])` crashes here — and is correctly failed.
- **Ties for the wettest day.** Two days can share the highest rainfall. The rule
  is deterministic: the **earliest** date in file order wins. A solution that uses
  `>=` instead of `>` picks the *last* tied day and is caught by the verifier,
  even though every other number it reports is correct.

These are the kinds of details that separate a real evaluation task from one that
gives full marks to sloppy work.

## Stress-testing the verifier

Oracle and nop only cover the two extremes: a fully correct solution and no solution at
all. `robustness/check_verifier.py` covers the space in between. It runs the real verifier
against solutions whose verdict is known in advance and checks that the verdict matches.

```
python3 robustness/check_verifier.py     # no Docker needed
```

| solution | what it does | verdict |
| --- | --- | --- |
| `solution/solve.py` | reference solution | pass |
| `equivalent_solutions/different_style.py` | correct, other code structure, key order and JSON formatting | pass |
| `wrong_solutions/naive_crash.py` | ignores malformed rows and crashes on `BROKEN` | fail |
| `wrong_solutions/malformed_as_zero.py` | counts malformed rows as 0.0 instead of skipping them | fail (criterion 2 only) |
| `wrong_solutions/wrong_tiebreak.py` | picks the last tied day instead of the earliest | fail (criterion 5 only) |
| `wrong_solutions/empty_report.py` | creates an empty report without doing the work | fail |
| `wrong_solutions/made_up_values.py` | writes a well-formed report with invented numbers | fail |

### Known gaps

The same harness found two wrong solutions that the verifier currently **passes**. They are
kept in `robustness/known_gaps/` so the limits of this task are stated, not hidden:

- **`hardcoded_answer.py`** writes the correct numbers without reading the data. The input
  file never changes, so the verifier cannot tell memorised answers from real work. Closing
  this needs inputs the agent has not seen, such as a second, hidden CSV at verify time.
- **`strict_threshold.py`** uses `> 50.0` instead of `>= 50.0`. No reading in the data is
  exactly 50.0, so the boundary of the rule is never exercised. Closing this needs a 50.0
  row in `rainfall.csv`.

## Layout

```
rainfall-report/
├── task.toml                # TB2 task config (metadata, limits, declared artifact)
├── instruction.md           # the brief given to the agent (numbered success criteria)
├── environment/
│   ├── Dockerfile           # base image pinned by @sha256 digest; bakes in pytest
│   └── rainfall.csv         # input data (includes malformed rows and a tie)
├── solution/
│   ├── solve.sh             # entrypoint the "oracle" runs
│   └── solve.py             # reference solution (handles both edge cases)
├── tests/
│   ├── test.sh              # runs pytest, writes reward.txt + ctrf.json
│   └── test_outputs.py      # one test per success criterion
└── robustness/
    ├── check_verifier.py    # runs the verifier against the solutions below
    ├── wrong_solutions/     # must fail
    ├── equivalent_solutions/# must pass
    └── known_gaps/          # wrong, but not detected yet
```

## Why this task is authored correctly

- **Reproducible environment.** Base image pinned by `@sha256` digest (a bare tag
  like `python:3.10-slim` isn't enough; `:latest` is never allowed), so the build
  is repeatable on any machine and any architecture.
- **No leaked solution.** The `solution/` directory is never copied into the
  agent's image.
- **No network at runtime.** `allow_internet = false`; every dependency is baked
  into the single Dockerfile.
- **A verifier that measures the real outcome.** `test_outputs.py` recomputes the
  expected numbers straight from `rainfall.csv` (applying the same edge-case rules)
  and asserts the produced values — it checks *what the report says*, not merely
  that a file exists.
- **Four-way consistency.** The output path is identical across `instruction.md`,
  the `task.toml` `artifacts` array, what the verifier asserts, and what
  `solve.py` writes (all `/app/report.json`).
- **One test per criterion.** Each of the five numbered criteria maps to exactly
  one test, named in the test's docstring. (Misaligned verifiers are the
  number-one failure mode in agent benchmarks.)

## How it's graded

A task is honest only if the reference solution passes **and** a do-nothing agent
fails:

```
harbor run -p rainfall-report -a oracle     # reference solution -> reward 1
harbor run -p rainfall-report --agent nop   # no-op agent        -> reward 0
```

Locally (mirroring that logic): running `solve.py` then `pytest` gives
**5 passed**; running `pytest` with no report gives **5 failed**.

## Notes

For the included `rainfall.csv`, the expected output is `total_rainfall_mm = 480.8`,
`valid_readings = 7`, `extreme_days = 5`, `wettest_day = "2024-04-29"` (the earlier
of two days tied at 103.6 mm; two rows are skipped as malformed).
