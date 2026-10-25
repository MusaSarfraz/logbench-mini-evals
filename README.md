# Log Summary Benchmark Tasks

Three small benchmark-style tasks for testing whether an AI model can fix and extend a broken Python script. Each task is a sealed Docker environment with a written instruction and hidden tests, in the same spirit as Terminal-Bench style tasks (built at a much smaller scale).

This is a learning project, not a rigorous benchmark. See [results.md](results.md) for exactly what was run and its limitations.

## What is a task?

Every task folder has the same four pieces:

| Piece | What it does |
|-------|--------------|
| `instruction.md` | Plain-English description of what the model must do |
| `Dockerfile` + `app/` | Builds the starting state: a broken `process_logs.py` and a `logs.txt` input |
| `tests/test_outputs.py` | Checks the end result (`/app/summary.json`) and nothing else |
| `solution.py` | Reference fix, which proves the task is solvable and the expected values are right |

The model sees only the instruction and the files in `app/`. The tests and the reference solution stay hidden.

## The tasks

| Task | What it tests |
|------|---------------|
| `benchmark-task-1` | Malformed lines and a strict line shape. A lazy fix counts garbage as a log level. |
| `benchmark-task-2` | Case-insensitive levels and usernames, real date validation (e.g. Feb 30), unknown levels, blank lines, extra spaces |
| `benchmark-task-3` | Everything in task 2 plus duplicate and out-of-order detection, which need state across lines and a stated check priority |

All tasks write a `summary.json` with counts per level, ERROR counts per user, and the number of skipped lines (task 3 adds `duplicates` and `out_of_order`).

## Run a task

Requires Docker Desktop. From inside a task folder (shown for task 1):

```
docker build -t task1 .

# 1. See the broken starting state (crashes with an IndexError)
docker run --rm task1 python process_logs.py

# 2. Check that the reference solution passes
docker run --rm -v "${PWD}\solution.py:/app/process_logs.py" -v "${PWD}\tests:/tests" task1 sh -c "python /app/process_logs.py && pytest /tests -q"
```

On Linux/macOS/Git Bash, replace `${PWD}\` with `$(pwd)/`.

## Grade a model's attempt

1. Paste the contents of `instruction.md`, `app/logs.txt` and `app/process_logs.py` into a fresh chat and ask for the full corrected `process_logs.py`.
2. Save the code to `attempt/process_logs.py` inside the task folder.
3. Run:

```
docker run --rm -v "${PWD}\attempt\process_logs.py:/app/process_logs.py" -v "${PWD}\tests:/tests" task1 sh -c "python /app/process_logs.py && pytest /tests -q"
```

## Results so far

Small and informal. Full detail in [results.md](results.md).

| Task | Model | Result |
|------|-------|--------|
| 2 | Claude Sonnet 5.5 | Pass |
| 3 | ChatGPT | Fail |

The task 3 failure is the interesting one. The model got the hard parts right (duplicate-before-out-of-order priority, case-sensitive actions, equal timestamps, date validation) but used a regex with a single literal space between fields, ignoring the instruction's "one or more spaces". One line was skipped, and that corrupted five output fields at once.

## Limitations

- One valid attempt per task, with different models on different tasks, so no pass rates or model comparisons.
- Attempts were one-shot in a chat window, not an agent working in a terminal.
- Task 1 has a verified reference solution but no valid model attempt yet.

## Layout

```
.
├── benchmark-task-1/
├── benchmark-task-2/
├── benchmark-task-3/
│   ├── app/            (logs.txt, broken process_logs.py)
│   ├── tests/          (test_outputs.py)
│   ├── Dockerfile
│   ├── instruction.md
│   └── solution.py
├── results.md
└── README.md
```