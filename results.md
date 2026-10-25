# Results

## Method

Each attempt is one-shot: the model receives the contents of `instruction.md`,
`app/logs.txt` and the broken `app/process_logs.py`, and must return a full
fixed `process_logs.py`. The attempt is saved to `attempt/process_logs.py` and
graded with pytest inside Docker:

    docker run --rm -v "${PWD}\attempt\process_logs.py:/app/process_logs.py" -v "${PWD}\tests:/tests" taskN sh -c "python /app/process_logs.py && pytest /tests -q"

Every task ships with a reference `solution.py` that passes the tests, which
shows the task is solvable and the expected values are correct.

A "valid" attempt means the model saw the real task files in a fresh chat.

## Tasks

| Task | What it tests | Reference solution |
|------|---------------|--------------------|
| 1 | Malformed lines, strict line shape (valid level, user=, action= prefixes) | Passes |
| 2 | Case-insensitive levels and users, real date validation, extra spaces, blank lines, unknown levels | Passes |
| 3 | Everything in task 2 plus duplicates and out-of-order lines (state across lines, check priority) | Passes |

## Attempts

| Task | Attempt | Model | Valid? | Result | Notes |
|------|---------|-------|--------|--------|-------|
| 1 | 1 | Claude | No | (not graded) | Prompt still contained the placeholders `<paste logs.txt>` and `<paste process_logs.py>`, so the model wrote a solution from the spec alone. Not a valid data point. |
| 2 | 1 | Claude Sonnet 5.5 | Yes | PASS | Handled case-insensitivity, invalid dates (2026-13-45, 2026-02-30), DEBUG level, blank line and extra spaces. |
| 3 | 1 | ChatGPT | Yes | FAIL | Regex used a single space between fields, ignoring "one or more spaces". |

### Summary

- Valid attempts: 2
- Passed: 1 (task 2, Claude Sonnet 5.5)
- Failed: 1 (task 3, ChatGPT)

## Failure details

### Task 3, attempt 1 (ChatGPT)

- Failing assertion: `levels`. ERROR was 4, expected 5.
- Cause: the regex separated fields with one literal space, so this line was
  rejected:
  `2026-10-01 10:02:30   ERROR   user=ali   action=upload`
- Effect: the line was counted as skipped, so `ali` was missing from
  `errors_by_user`, and a later repeat of the same line was counted as
  out_of_order instead of duplicate.
- Verdict: model error. The instruction states the rule ("one or more
  spaces") and the reference solution handles it.
- Things it got right: duplicate-before-out-of-order priority, case-sensitive
  actions, equal timestamps not counted as out of order, date validation.

## Observations

- Task 2 was solved cleanly: every rule was listed in the instruction and
  the model implemented all of them.
- Task 3 added state across lines and was failed, but not because of the new
  rules. The model handled duplicates and ordering correctly and missed a plain
  whitespace rule.
- One missed rule corrupted several output fields at once (levels,
  errors_by_user, skipped, duplicates, out_of_order).

## Limitations

- Sample size is tiny (one valid attempt per task, one model per task).
- Attempts were one-shot in a chat window, not an agent working inside a
  terminal, so results are not comparable to Terminal-Bench style runs.
- Different models were used on different tasks, so pass rates cannot be
  compared across tasks.

## Next

- Grade the task 1 attempt properly with the real files pasted in a fresh chat.
- Run the same task 3 prompt on Claude and ChatGPT a few more times each.