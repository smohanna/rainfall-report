# rainfall-report — an AI-agent evaluation task for extreme-rainfall data

A self-authored **evaluation task** for AI coding agents, in the Terminal-Bench 2
(Harbor) format, applied to a climate problem: turning a CSV of daily rainfall
readings into a JSON summary that flags extreme-rain days.

The point of this repo isn't the ETL — it's the **evaluation**. As AI agents take
on real work with climate and weather data, we need tasks that measure whether an
agent *actually* produced the right numbers, in an environment that runs the same
way everywhere. This is a compact, honestly-graded example of exactly that.

> Self-authored with synthetic data. Independent portfolio work — not affiliated
> with or derived from any employer or organization.

## What the task asks

Given `/app/rainfall.csv` (columns: `date, station, rainfall_mm`), produce
`/app/report.json` with exactly:

| key                 | type    | meaning                                              |
| ------------------- | ------- | ---------------------------------------------------- |
| `total_rainfall_mm` | number  | sum of `rainfall_mm`, rounded to 2 dp                |
| `day_count`         | integer | number of data rows (header and blanks excluded)     |
| `extreme_days`      | integer | rows with `rainfall_mm >= 50.0` (the extreme threshold) |
| `wettest_day`       | string  | `date` of the row with the highest `rainfall_mm`     |

## Layout

```
rainfall-report/
├── task.toml                # TB2 task config (metadata, limits, declared artifact)
├── instruction.md           # the brief given to the agent (numbered success criteria)
├── environment/
│   ├── Dockerfile           # base image pinned by @sha256 digest; bakes in pytest
│   └── rainfall.csv         # input data
├── solution/
│   ├── solve.sh             # entrypoint the "oracle" runs
│   └── solve.py             # reference solution
└── tests/
    ├── test.sh              # runs pytest, writes reward.txt + ctrf.json
    └── test_outputs.py      # one test per success criterion
```

## Why this task is authored correctly

Getting an evaluation task *right* is the hard part. This one satisfies every
property a trustworthy agent benchmark needs:

- **Reproducible environment.** The base image is pinned by `@sha256` digest (a
  bare tag like `python:3.10-slim` isn't enough; `:latest` is never allowed), so
  the build is repeatable on any machine and any architecture.
- **No leaked solution.** The `solution/` directory is never copied into the
  agent's image.
- **No network at runtime.** `allow_internet = false`; every dependency is baked
  into the single Dockerfile.
- **A verifier that measures the real outcome.** `test_outputs.py` recomputes the
  expected numbers straight from `rainfall.csv` and asserts the produced values —
  it checks *what the report says*, not merely that a file exists.
- **Four-way consistency.** The output path is identical across `instruction.md`,
  the `task.toml` `artifacts` array, what the verifier asserts, and what
  `solve.py` writes (all `/app/report.json`).
- **One test per criterion.** Each of the five numbered criteria in
  `instruction.md` maps to exactly one test, named in the test's docstring.
  (Misaligned verifiers are the number-one failure mode in agent benchmarks.)

## How it's graded

A task is honest only if the reference solution passes **and** a do-nothing agent
fails:

```
harbor run -p rainfall-report -a oracle     # reference solution -> reward 1
harbor run -p rainfall-report --agent nop   # no-op agent        -> reward 0
```

Locally (mirroring that logic): running `solve.py` then `pytest` gives
**5 passed**; running `pytest` with no report produced gives **5 failed**.

## Notes

For the included `rainfall.csv`, the expected output is `total_rainfall_mm = 440.8`,
`day_count = 9`, `extreme_days = 5`, `wettest_day = "2024-05-01"`.
