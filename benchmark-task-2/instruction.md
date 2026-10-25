The script /app/process_logs.py reads /app/logs.txt and should write
/app/summary.json with exactly these keys:

- "levels": dict of how many valid lines exist per level
- "errors_by_user": dict of how many ERROR lines each user has
- "skipped": the number of malformed lines that were ignored

A valid line looks like: DATE TIME LEVEL user=NAME action=ACTION

Rules:
- Fields are separated by one or more spaces.
- DATE (YYYY-MM-DD) and TIME (HH:MM:SS) must be a real date and time.
- Allowed levels are INFO, WARN and ERROR, in any letter case.
  Report levels in uppercase.
- Usernames are case-insensitive. Report them in lowercase.
- Blank lines are ignored and are not counted as skipped.
- Every other non-blank line is malformed: skip it and count it.

Fix and extend the script, then run it once so /app/summary.json exists.