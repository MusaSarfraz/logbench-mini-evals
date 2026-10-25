The script /app/process_logs.py reads /app/logs.txt and should write
/app/summary.json with exactly these keys:

- "levels": dict of how many accepted lines exist per level
- "errors_by_user": dict of how many accepted ERROR lines each user has
- "skipped": number of malformed lines
- "duplicates": number of duplicate lines
- "out_of_order": number of out-of-order lines

A line has the form: DATE TIME LEVEL user=NAME action=ACTION

Rules:
- Fields are separated by one or more spaces.
- DATE (YYYY-MM-DD) and TIME (HH:MM:SS) must be a real date and time.
- Allowed levels are INFO, WARN and ERROR, in any letter case.
  Report levels in uppercase.
- Usernames are case-insensitive. Report them in lowercase.
  Actions are case-sensitive.
- Blank lines are ignored and not counted anywhere.
- A non-blank line that does not fit the form above is malformed:
  count it in "skipped".
- Process lines in file order. A well-formed line is a duplicate if an
  earlier accepted line has the same timestamp, level, user and action
  (after the normalisation above). Count it in "duplicates".
- A well-formed, non-duplicate line is out of order if its timestamp is
  earlier than the latest timestamp among lines accepted so far.
  Count it in "out_of_order". An equal timestamp is not out of order.
- Every other line is accepted and counted in levels/errors_by_user.
- A line is counted in only one of skipped, duplicates, out_of_order
  or accepted. Check in that order.

Fix and extend the script, then run it once so /app/summary.json exists.